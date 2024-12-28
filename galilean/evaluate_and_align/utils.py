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
    
    weights = np.array([0.25, 0.45, 0.30])
    scores = np.sum(normalized * weights, axis=1)
    avg_quality = np.mean(scores)
    return scores, avg_quality

def select_template(images: np.ndarray) -> Tuple[int, np.ndarray, float, float]:
    """Select best template based on quality score."""
    scores, avg_quality = evaluate_image_quality(images)
    best_index = np.argmax(scores)
    return best_index, images[best_index], scores[best_index], avg_quality

def phase_correlation_align(template: np.ndarray, image: np.ndarray) -> Tuple[np.ndarray]:
    """Align image to template using phase correlation for translation only."""
    if np.array_equal(template, image):
        return image

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
    aligned = cv2.warpAffine(image, M, (w, h), borderValue=0)

    return aligned