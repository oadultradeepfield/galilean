import numpy as np

from postprocessing.utils import calibrate_color, selective_sharpening


def postprocessing(image: np.ndarray, sharpening_factor: float = 1.5) -> np.ndarray:
    """Processes color planetary image with calibration and sharpening"""
    processed = calibrate_color(image)
    processed = selective_sharpening(processed, sharpening_factor)
    return processed
