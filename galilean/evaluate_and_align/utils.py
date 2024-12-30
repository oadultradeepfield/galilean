from typing import Tuple

import cv2
import numpy as np


def evaluate_image_quality(images: np.ndarray) -> Tuple[np.ndarray, float]:
    """Evaluate quality metrics for all images and return normalized scores and average quality."""
    all_metrics = []
    for image in images:
        grayscale = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        contrast = np.std(grayscale)
        sharpness = cv2.Laplacian(grayscale, cv2.CV_64F).var()
        snr = np.mean(grayscale) / (np.std(grayscale) + 1e-8)
        all_metrics.append([contrast, sharpness, snr])
    
    metrics_array = np.array(all_metrics)
    min_vals = np.min(metrics_array, axis=0)
    max_vals = np.max(metrics_array, axis=0)
    normalized = (metrics_array - min_vals) / (max_vals - min_vals + 1e-8)
    
    weights = np.array([0.2, 0.5, 0.3])
    scores = np.sum(normalized * weights, axis=1)
    avg_quality = np.mean(scores)
    return scores, avg_quality

def select_template(images: np.ndarray, threshold: float = 0.95) -> Tuple[int, np.ndarray, float, float, int]:
    """Select best template based on quality score and also return the top images based on threshold."""
    scores, avg_quality = evaluate_image_quality(images)
    best_index = np.argmax(scores)
    sorted_indices = np.argsort(scores)[::-1]
    num_top_images = int(len(images) * threshold)
    top_images_indices = sorted_indices[:num_top_images]
    return best_index, images[best_index], scores[best_index], avg_quality, top_images_indices

def align_image_to_template(template: np.ndarray, image: np.ndarray) -> np.ndarray:
    """Aligns an input image to a template image using ECC maximization."""
    template_gray = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
    image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    warp_mode = cv2.MOTION_TRANSLATION
    warp_matrix = np.eye(2, 3, dtype=np.float32)
    
    criteria = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 5000, 1e-10)
    
    _, warp_matrix = cv2.findTransformECC(
        template_gray, 
        image_gray,
        warp_matrix, 
        warp_mode, 
        criteria
    )
    
    return cv2.warpAffine(
        image,
        warp_matrix, 
        (template.shape[1], template.shape[0]),
        flags=cv2.INTER_LINEAR + cv2.WARP_INVERSE_MAP
    )
