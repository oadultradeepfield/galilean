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


def test_multiple_images(test_paths: List[str], out_dir: str, crop_size: int = 448) -> None:
    """Process multiple test images using detect_and_crop."""
    for test_path in test_paths:
        try:
            test_detect_and_crop(test_path, out_dir, crop_size)
            print(f"Successfully processed: {test_path}")
        except Exception as e:
            print(f"Failed to process {test_path}: {str(e)}")


if __name__ == "__main__":
    test_paths = [
        "test/source/sample_frame_moon.png",
        "test/source/sample_frame_jupiter.png",
        "test/source/sample_frame_saturn.png"
    ]
    out_dir = "test/out/io"
    test_multiple_images(test_paths, out_dir)
