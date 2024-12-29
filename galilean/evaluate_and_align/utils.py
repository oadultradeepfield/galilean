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

def select_template(images: np.ndarray, threshold: float = 0.95) -> Tuple[int, np.ndarray, float, float]:
    """Select best template based on quality score and also return the top images based on threshold."""
    scores, avg_quality = evaluate_image_quality(images)
    best_index = np.argmax(scores)
    sorted_indices = np.argsort(scores)[::-1]
    num_top_images = int(len(images) * threshold)
    top_images_indices = sorted_indices[:num_top_images]
    return best_index, images[best_index], scores[best_index], avg_quality, top_images_indices

def phase_correlation_align(template: np.ndarray, image: np.ndarray) -> Tuple[np.ndarray]:
    """Align image to template using phase correlation for translation only."""
    h, w = template.shape[:2]

    template_gray = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
    image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    fft_template = np.fft.fft2(template_gray)
    fft_image = np.fft.fft2(image_gray)
    correlation = fft_template * np.conj(fft_image)
    correlation /= (np.abs(correlation) + 1e-8)
    shift = np.fft.ifft2(correlation)
    shift = np.abs(shift)

    y_shift, x_shift = np.unravel_index(np.argmax(shift), shift.shape)
    if y_shift > h // 2:
        y_shift -= h
    if x_shift > w // 2:
        x_shift -= w

    M = np.float32([[1, 0, x_shift], [0, 1, y_shift]])
    aligned = cv2.warpAffine(image, M, (w, h), borderMode=cv2.BORDER_REPLICATE)

    return aligned
