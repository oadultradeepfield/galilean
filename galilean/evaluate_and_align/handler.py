from typing import List, Tuple

import numpy as np

from evaluate_and_align.utils import phase_correlation_align, select_template


def evaluate_and_align(images: List[np.ndarray]) -> Tuple[np.ndarray, int, float, float]:
    """Align all images to template and return aligned images and their shifts."""
    best_index, best_image, best_score, avg_quality = select_template(images)
    
    aligned_images = []
    
    for image in images:
        aligned = phase_correlation_align(best_image, image)
        aligned_images.append(aligned)
    
    return aligned_images, best_index, best_score, avg_quality
