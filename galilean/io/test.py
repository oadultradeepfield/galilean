import os
from typing import List

import cv2
from handler import detect_and_crop


def test_detect_and_crop(image_path: str, out_dir: str, crop_size: int = 480) -> None:
    """
    Test the detect_and_crop function by processing an image and saving the result.
    
    Args:
        image_path: Path to the input image file
        out_dir: Directory where the processed image will be saved
        crop_size: Size of the square crop in pixels (default: 480)
        
    Raises:
        FileNotFoundError: If the input image doesn't exist
        ValueError: If the output directory can't be created
        Exception: If image processing fails
    """
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
    """
    Process multiple test images using detect_and_crop.
    
    Args:
        test_paths: List of paths to test images
        out_dir: Directory where processed images will be saved
        crop_size: Size of the square crop in pixels (default: 448)
    """
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
