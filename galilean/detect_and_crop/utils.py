from typing import Union

import cv2
import numpy as np


def read_image(source: Union[str, np.ndarray]) -> np.ndarray:
    """Read an image from either a file path or numpy array."""
    if isinstance(source, str):
        image = cv2.imread(source, cv2.IMREAD_COLOR)
        if image is None:
            raise ValueError(f"Could not load image from path: {source}")
        return image
    return source.copy()

def get_grayscale(image: np.ndarray) -> np.ndarray:
    """Convert an image to grayscale if it's in color, or return a copy if already grayscale."""
    if len(image.shape) == 3:
        return cv2.cvtColor(image.astype(np.uint8), cv2.COLOR_BGR2GRAY)
    return image.copy()

def get_binary(grayscale_image: np.ndarray) -> np.ndarray:
    """Apply adaptive thresholding to create a binary image."""
    binary_image =  cv2.adaptiveThreshold(
        grayscale_image,
        255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY_INV,
        11,
        2
    )
    
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    return cv2.dilate(binary_image, kernel, iterations=1)
