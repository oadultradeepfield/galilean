from typing import Union

import cv2
import numpy as np


def read_image(source: Union[str, np.ndarray]) -> np.ndarray:
    """
    Read an image from either a file path or numpy array.
    
    Args:
        source: Either a path to an image file (str) or a numpy array containing the image
        
    Returns:
        np.ndarray: A copy of the loaded image in BGR color format
        
    Raises:
        ValueError: If the image file cannot be loaded from the provided path
    """
    if isinstance(source, str):
        image = cv2.imread(source, cv2.IMREAD_COLOR)
        if image is None:
            raise ValueError(f"Could not load image from path: {source}")
        return image
    return source.copy()


def get_grayscale(image: np.ndarray) -> np.ndarray:
    """
    Convert an image to grayscale if it's in color, or return a copy if already grayscale.
    
    Args:
        image: Input image as numpy array (can be either BGR or grayscale)
        
    Returns:
        np.ndarray: Grayscale version of the input image
    """
    if len(image.shape) == 3:
        return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    return image.copy()


def get_binary(grayscale_image: np.ndarray) -> np.ndarray:
    """
    Apply adaptive thresholding to create a binary image.
    
    Args:
        grayscale_image: Input grayscale image as numpy array
        
    Returns:
        np.ndarray: Binary image created using Gaussian adaptive thresholding
        
    Notes:
        Uses Gaussian adaptive thresholding with:
        - Max value: 255
        - Block size: 11
        - Constant subtracted from mean: 2
    """
    return cv2.adaptiveThreshold(
        grayscale_image,
        255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY_INV,
        11,
        2
    )
