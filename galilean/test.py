import os
from typing import List, Tuple

import cv2
import numpy as np

from detect_and_crop.handler import detect_and_crop
from evaluate_and_align.handler import evaluate_and_align
from image_stacking.handler import image_stacking
from postprocessing.handler import postprocessing


def load_images(directory: str) -> List[Tuple[np.ndarray, str]]:
    if not os.path.exists(directory):
        raise FileNotFoundError(f"Input directory not found: {directory}")
    
    images = []
    for file in sorted(os.listdir(directory)):
        file_path = os.path.join(directory, file)
        if os.path.isfile(file_path):
            image = cv2.imread(file_path, cv2.IMREAD_COLOR)
            if image is not None:
                images.append((image, file_path))
    
    if not images:
        raise ValueError(f"No valid images found in directory: {directory}")
    return images

def save_image(image: np.ndarray, path: str, suffix: str) -> str:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    base, ext = os.path.splitext(os.path.basename(path))
    out_path = os.path.join(os.path.dirname(path), f"{base}_{suffix}{ext}")
    if not cv2.imwrite(out_path, image.astype(np.uint8)):
        raise Exception(f"Failed to save image to: {out_path}")
    return out_path

def process_images(input_dir: str, output_base_dir: str) -> None:
    test_dirs = [os.path.join(input_dir, d) for d in ["moon_sample_frames", 
                                                     "jupiter_sample_frames", 
                                                     "saturn_sample_frames"]]
    
    for test_dir in test_dirs:
        try:
            folder_name = os.path.basename(test_dir)
            images, paths = zip(*load_images(test_dir))
            
            align_dir = os.path.join(output_base_dir, "align", folder_name)
            aligned_images, _, _, _ = evaluate_and_align(images, 0.95)
            for img, path in zip(aligned_images, paths):
                save_image(img, os.path.join(align_dir, os.path.basename(path)), "aligned")
            
            stack_dir = os.path.join(output_base_dir, "stack", folder_name)
            stacked = image_stacking(np.array(aligned_images), "mean_with_median_clipping")
            save_image(stacked, os.path.join(stack_dir, "result.png"), "stacked")
            
            crop_dir = os.path.join(output_base_dir, "crop", folder_name)
            cropped = detect_and_crop(stacked, 480)
            save_image(cropped, os.path.join(crop_dir, "result.png"), "cropped")
            
            post_dir = os.path.join(output_base_dir, "post", folder_name)
            processed = postprocessing(cropped, 1.5, 2)
            save_image(processed, os.path.join(post_dir, "result.png"), "postprocessed")
            
        except Exception as e:
            print(f"Failed to process {test_dir}: {str(e)}")

if __name__ == "__main__":
    process_images("test/input", "test/out")
