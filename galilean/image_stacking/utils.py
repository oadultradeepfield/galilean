import numpy as np


def mean_image_stacking(images: np.ndarray) -> np.ndarray:
    """Stack all images using average (mean) stacking."""
    return np.mean(images, axis=0)

def median_image_stacking(images: np.ndarray) -> np.ndarray:
    """Stack all images using median stacking."""
    return np.median(images, axis=0)

def mean_image_stacking_with_clipping(images: np.ndarray, kappa: float = 3.0) -> np.ndarray:
    """Stack images by rejecting the pixel value that have value beyond threshold (mean +/- kappa * sigma)."""
    mean = np.mean(images, axis=0)
    sigma = np.std(images, axis=0)
    lower_bound = mean - kappa * sigma
    upper_bound = mean + kappa * sigma
    clipped_images = np.clip(images, lower_bound, upper_bound)
    return np.mean(clipped_images, axis=0)

def mean_image_stacking_with_median_clipping(images: np.ndarray, kappa: float = 3.0) -> np.ndarray:
    """Stack images by changing the pixel value that have value beyond threshold (mean +/- kappa * sigma) with median value."""
    mean = np.mean(images, axis=0)
    sigma = np.std(images, axis=0)
    lower_bound = mean - kappa * sigma
    upper_bound = mean + kappa * sigma
    median_value = np.median(images, axis=0)
    clipped_images = np.where((images < lower_bound) | (images > upper_bound), median_value, images)
    return np.mean(clipped_images, axis=0)
