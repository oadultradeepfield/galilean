import os
from typing import List

import cv2
import numpy as np

from detect_and_crop.handler import detect_and_crop
from evaluate_and_align.handler import evaluate_and_align
from image_stacking.handler import image_stacking
from postprocessing.handler import postprocessing


def test_detect_and_crop(image_path: str, out_dir: str, crop_size: int = 480) -> None:
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Input image not found: {image_path}")

    os.makedirs(out_dir, exist_ok=True)

    result = detect_and_crop(image_path, crop_size)

    filename = os.path.basename(image_path)
    base, ext = os.path.splitext(filename)
    out_path = os.path.join(out_dir, f"{base}_cropped{ext}")

    if not cv2.imwrite(out_path, result):
        raise Exception(f"Failed to save image to: {out_path}")

def process_directory(test_dir: str, out_base_dir: str, crop_size: int = 480) -> None:
    if not os.path.exists(test_dir):
        raise FileNotFoundError(f"Input directory not found: {test_dir}")

    folder_name = os.path.basename(test_dir)
    out_dir = os.path.join(out_base_dir, folder_name)

    for root, _, files in os.walk(test_dir):
        for file in files:
            file_path = os.path.join(root, file)
            relative_dir = os.path.relpath(root, test_dir)
            nested_out_dir = os.path.join(out_dir, relative_dir)

            try:
                test_detect_and_crop(file_path, nested_out_dir, crop_size)
                print(f"Successfully processed: {file_path}")
            except Exception as e:
                print(f"Failed to process {file_path}: {str(e)}")

def test_multiple_directories(test_dirs: List[str], out_base_dir: str, crop_size: int = 480) -> List[str]:
    output_dirs = []
    for test_dir in test_dirs:
        try:
            process_directory(test_dir, out_base_dir, crop_size)
            output_dirs.append(os.path.join(out_base_dir, os.path.basename(test_dir)))
        except Exception as e:
            print(f"Failed to process directory {test_dir}: {str(e)}")
    return output_dirs

def test_evaluate_and_align(input_dir: str, output_dir: str, threshold: float=0.95) -> None:
    if not os.path.exists(input_dir):
        raise FileNotFoundError(f"Input directory not found: {input_dir}")

    os.makedirs(output_dir, exist_ok=True)

    images = []
    image_paths = []
    for file in sorted(os.listdir(input_dir)):
        file_path = os.path.join(input_dir, file)
        if os.path.isfile(file_path):
            image = cv2.imread(file_path, cv2.IMREAD_COLOR)
            if image is not None:
                images.append(image)
                image_paths.append(file_path)

    if not images:
        raise ValueError(f"No valid images found in directory: {input_dir}")

    aligned_images, best_index, best_score, avg_quality = evaluate_and_align(images, threshold)

    for aligned_image, original_path in zip(aligned_images, image_paths):
        filename = os.path.basename(original_path)
        base, ext = os.path.splitext(filename)
        out_path = os.path.join(output_dir, f"{base}_aligned{ext}")
        if not cv2.imwrite(out_path, aligned_image):
            raise Exception(f"Failed to save aligned image to: {out_path}")

    print(f"Alignment completed for {input_dir}. Best index: {best_index}, Best score: {best_score:.2f}, Avg quality: {avg_quality:.2f}")

def test_image_stacking(input_dir: str, output_dir: str, method: str = "mean_with_median_clipping") -> None:
    if not os.path.exists(input_dir):
        raise FileNotFoundError(f"Input directory not found: {input_dir}")

    os.makedirs(output_dir, exist_ok=True)

    images = []
    for file in sorted(os.listdir(input_dir)):
        file_path = os.path.join(input_dir, file)
        if os.path.isfile(file_path):
            image = cv2.imread(file_path, cv2.IMREAD_COLOR)
            if image is not None:
                images.append(image)

    if not images:
        raise ValueError(f"No valid images found in directory: {input_dir}")

    result = image_stacking(np.array(images), method)

    path_parts = input_dir.split("/")
    try:
        out_index = path_parts.index("out")
        relative_path = "_".join(path_parts[out_index + 1:])
    except ValueError:
        relative_path = "_".join(path_parts)
    
    out_path = os.path.join(output_dir, f"{relative_path}_stacked.png")
    
    if not cv2.imwrite(out_path, result):
        raise Exception(f"Failed to save stacked image to: {out_path}")
    
    print(f"Successfully stacked and enhanced images from {input_dir}")
    
def test_postprocessing(input_dir: str, output_dir: str, sharpening_factor: float = 1.5, scaling_factor: int = 2) -> None:
    """Tests post-processing pipeline on planetary images with color calibration, sharpening and super-resolution"""
    if not os.path.exists(input_dir):
        raise FileNotFoundError(f"Input directory not found: {input_dir}")
    
    os.makedirs(output_dir, exist_ok=True)
    
    for file in os.listdir(input_dir):
        if file.endswith("_stacked.png"):
            file_path = os.path.join(input_dir, file)
            image = cv2.imread(file_path)
            
            if image is None:
                print(f"Failed to read image: {file_path}")
                continue
                
            try:
                processed_image = postprocessing(image, sharpening_factor, scaling_factor)
                base_name = os.path.splitext(file)[0]
                out_path = os.path.join(output_dir, f"{base_name}_postprocessed.png")
                
                if not cv2.imwrite(out_path, processed_image):
                    raise Exception(f"Failed to save processed image to: {out_path}")
                    
                print(f"Successfully post-processed: {file_path}")
                
            except Exception as e:
                print(f"Failed to process {file_path}: {str(e)}")

if __name__ == "__main__":
    test_dirs = [
        "test/input/moon_sample_frames",
        "test/input/jupiter_sample_frames",
        "test/input/saturn_sample_frames"
    ]
    out_base_dir = "test/out/detect_and_crop"
    align_base_dir = "test/out/evaluate_and_align"
    stack_base_dir = "test/out/image_stacking"
    post_base_dir = "test/out/postprocessing"

    os.makedirs(stack_base_dir, exist_ok=True)
    cropped_dirs = test_multiple_directories(test_dirs, out_base_dir)

    for cropped_dir in cropped_dirs:
        dir_name = os.path.basename(cropped_dir)
        align_dir = os.path.join(align_base_dir, dir_name)
        
        try:
            test_evaluate_and_align(cropped_dir, align_dir)
            test_image_stacking(align_dir, stack_base_dir)
        except Exception as e:
            print(f"Failed to process {cropped_dir}: {str(e)}")
    
    try:
        test_postprocessing(stack_base_dir, post_base_dir)
    except Exception as e:
            print(f"Failed to process {stack_base_dir}: {str(e)}")
