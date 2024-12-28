import numpy as np

from postprocessing.utils import calibrate_color, images_sr, laplacian_sharpen


def postprocessing(image: np.ndarray, sharpening_factor: float = 1.5, scaling_factor: int = 2) -> np.ndarray:
    """Processes color planetary image with calibration, sharpening, and super resolution"""
    if scaling_factor > 1:
        image = images_sr(image, scaling_factor)
        
    processed = calibrate_color(image)
    processed = laplacian_sharpen(processed, sharpening_factor)
    return processed
