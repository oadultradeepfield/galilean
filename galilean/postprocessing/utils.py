import cv2
import numpy as np
import pywt


def calibrate_color(image: np.ndarray) -> np.ndarray:
    """Performs auto color correction using Gray World Assumption"""
    avg_bgr = np.mean(image, axis=(0, 1))
    scale = np.mean(avg_bgr) / avg_bgr
    return cv2.convertScaleAbs(image * scale)

def selective_sharpening(image: np.ndarray, sharpening_factor: float = 1.5) -> np.ndarray:
    """Sharpens only regions with detected objects using adaptive unsharp masking"""
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    local_contrast = cv2.Laplacian(gray, cv2.CV_64F)
    mask = cv2.normalize(local_contrast, None, 0, 1, cv2.NORM_MINMAX)
    mask = cv2.merge([mask] * 3)
    sharpened = cv2.addWeighted(image, 1 + sharpening_factor, cv2.GaussianBlur(image, (5, 5), 0), -sharpening_factor, 0)
    return cv2.convertScaleAbs(image * (1 - mask) + sharpened * mask)

def images_sr(image: np.ndarray, scaling_factor: int = 2) -> np.ndarray:
    sr_model = cv2.dnn_superres.DnnSuperResImpl_create()
    model_path = f"models/EDSR_x{scaling_factor}.pb"
    sr_model.readModel(model_path)
    sr_model.setModel("edsr", scaling_factor)
    scaled_image = sr_model.upsample(image)
    return scaled_image
