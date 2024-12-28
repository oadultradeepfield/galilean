import os
from typing import List

import cv2

from detect_and_crop.handler import detect_and_crop
from evaluate_and_align.handler import evaluate_and_align


def test_detect_and_crop(image_path: str, out_dir: str, crop_size: int = 448) -> None:
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Input image not found: {image_path}")

    os.makedirs(out_dir, exist_ok=True)

    result = detect_and_crop(image_path, crop_size)

    filename = os.path.basename(image_path)
    base, ext = os.path.splitext(filename)
    out_path = os.path.join(out_dir, f"{base}_cropped{ext}")

    if not cv2.imwrite(out_path, result):
        raise Exception(f"Failed to save image to: {out_path}")

def process_directory(test_dir: str, out_base_dir: str, crop_size: int = 448) -> None:
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

def test_multiple_directories(test_dirs: List[str], out_base_dir: str, crop_size: int = 448) -> List[str]:
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

if __name__ == "__main__":
    test_dirs = [
        "test/input/moon_sample_frames",
        "test/input/jupiter_sample_frames",
        "test/input/saturn_sample_frames"
    ]
    out_base_dir = "test/out/detect_and_crop"
    align_base_dir = "test/out/evaluate_and_align"
    quality_threshold = 0.95

    cropped_dirs = test_multiple_directories(test_dirs, out_base_dir)

    for cropped_dir in cropped_dirs:
        align_dir = os.path.join(align_base_dir, os.path.basename(cropped_dir))
        try:
            test_evaluate_and_align(cropped_dir, align_dir, quality_threshold)
        except Exception as e:
            print(f"Failed to align images in {cropped_dir}: {str(e)}")
