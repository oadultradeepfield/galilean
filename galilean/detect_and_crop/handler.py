from typing import Tuple, Union

import cv2
import numpy as np

from detect_and_crop.utils import get_binary, get_grayscale, read_image


def detect_and_crop(
    source: Union[str, np.ndarray],
    crop_size: int,
    padding_color: Tuple[int, int, int] = (0, 0, 0)
) -> np.ndarray:
    """Detect the centroid of an object in an image and crop around it, 
    padding with a specified color if needed."""
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
        
    result = np.full((crop_size, crop_size, 3), padding_color, dtype=np.uint8)
    half_size = crop_size // 2
    
    src_x_min = max(centroid_x - half_size, 0)
    src_y_min = max(centroid_y - half_size, 0)
    src_x_max = min(centroid_x + half_size, w)
    src_y_max = min(centroid_y + half_size, h)
    
    dst_x_min = half_size - (centroid_x - src_x_min)
    dst_y_min = half_size - (centroid_y - src_y_min)
    dst_x_max = dst_x_min + (src_x_max - src_x_min)
    dst_y_max = dst_y_min + (src_y_max - src_y_min)
    
    result[dst_y_min:dst_y_max, dst_x_min:dst_x_max] = image[src_y_min:src_y_max, src_x_min:src_x_max]
    return result
