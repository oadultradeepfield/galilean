import os
from typing import List

import cv2
from handler import detect_and_crop


def test_detect_and_crop(image_path: str, out_dir: str, crop_size: int = 448) -> None:
    """Test the detect_and_crop function by processing an image and saving the result."""
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
    """Process all images in a directory and save the results in corresponding output directories."""
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

def test_multiple_directories(test_dirs: List[str], out_base_dir: str, crop_size: int = 448) -> None:
    """Process images in multiple directories."""
    for test_dir in test_dirs:
        try:
            process_directory(test_dir, out_base_dir, crop_size)
        except Exception as e:
            print(f"Failed to process directory {test_dir}: {str(e)}")

if __name__ == "__main__":
    test_dirs = [
        "test/input/moon_sample_frames",
        "test/input/jupiter_sample_frames",
        "test/input/saturn_sample_frames"
    ]
    out_base_dir = "test/out/io"
    test_multiple_directories(test_dirs, out_base_dir)
