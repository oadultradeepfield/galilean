from typing import Union

import cv2
import numpy as np

from detect_and_crop.utils import get_binary, get_grayscale, read_image


def detect_and_crop(
    source: Union[str, np.ndarray],
    crop_size: int,
) -> np.ndarray:
    """Detect the centroid of an object in an image and crop around it, 
    padding with interpolated edges if needed."""
    image = read_image(source)
    binary = get_binary(get_grayscale(image))
    
    M = cv2.moments(binary)
    if M["m00"] == 0:
        raise Exception("No object detected in the image")
    
    centroid_x = int(M["m10"] / M["m00"])
    centroid_y = int(M["m01"] / M["m00"])
    
    h, w = image.shape[:2]
    min_dimension = min(h, w)
    if crop_size > min_dimension:
        crop_size = min_dimension
        
    half_size = crop_size // 2
    
    src_x_min = max(centroid_x - half_size, 0)
    src_y_min = max(centroid_y - half_size, 0)
    src_x_max = min(centroid_x + half_size, w)
    src_y_max = min(centroid_y + half_size, h)
    
    cropped = image[src_y_min:src_y_max, src_x_min:src_x_max]
    
    top = max(0, half_size - centroid_y)
    bottom = max(0, centroid_y + half_size - h)
    left = max(0, half_size - centroid_x)
    right = max(0, centroid_x + half_size - w)
    
    result = cv2.copyMakeBorder(
        cropped,
        top=top,
        bottom=bottom,
        left=left,
        right=right,
        borderType=cv2.BORDER_REPLICATE
    )
    
    result = cv2.resize(result, (crop_size, crop_size), interpolation=cv2.INTER_LINEAR)
    return result
