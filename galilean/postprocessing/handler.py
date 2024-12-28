import numpy as np

from postprocessing.utils import (calibrate_color, images_sr,
                                  selective_sharpening)


def postprocessing(image: np.ndarray, sharpening_factor: float = 1.5, scaling_factor: int = 2) -> np.ndarray:
    """Processes color planetary image with calibration and sharpening"""
    if scaling_factor > 1:
        image = images_sr(image, scaling_factor)
        
    processed = calibrate_color(image)
    processed = selective_sharpening(processed, sharpening_factor)
    return processed
