import numpy as np

from postprocessing.utils import (calibrate_color, images_sr,
                                  selective_sharpening)


def postprocessing(image: np.ndarray, sharpening_factor: float = 1.5, scaling_factor: int = 2) -> np.ndarray:
    """Processes color planetary image with calibration, sharpening, and super resolution"""
    processed = calibrate_color(image)
    processed = selective_sharpening(processed, sharpening_factor)
    
    if scaling_factor > 1:
        processed = images_sr(processed, scaling_factor)
        
    return processed
