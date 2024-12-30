from typing import List, Tuple

import numpy as np

from evaluate_and_align.utils import align_image_to_template, select_template


def evaluate_and_align(images: List[np.ndarray], threshold: float=0.95) -> Tuple[np.ndarray, int, float, float]:
    """Align all images to template and return aligned images and their shifts."""
    best_index, best_image, best_score, avg_quality, top_images_indices = select_template(images, threshold)
    
    aligned_images = []
    
    for index, image in enumerate(images):
        if index in top_images_indices:
            aligned = align_image_to_template(best_image, image)
            aligned_images.append(aligned)
    
    return aligned_images, best_index, best_score, avg_quality
