import cv2
import numpy as np


def calibrate_color(image: np.ndarray) -> np.ndarray:
    """Performs auto color correction using Gray World Assumption"""
    calibrated = cv2.cvtColor(image.astype(np.uint8), cv2.COLOR_BGR2LAB)
    avg_a = np.average(calibrated[:, :, 1])
    avg_b = np.average(calibrated[:, :, 2])
    calibrated[:, :, 1] = calibrated[:, :, 1] - ((avg_a - 128) * (calibrated[:, :, 0] / 255.0) * 1.1)
    calibrated[:, :, 2] = calibrated[:, :, 2] - ((avg_b - 128) * (calibrated[:, :, 0] / 255.0) * 1.1)
    calibrated = cv2.cvtColor(calibrated.astype(np.uint8), cv2.COLOR_LAB2BGR)
    return calibrated

def laplacian_sharpen(image: np.ndarray, sharpening_factor: float = 1.5) -> np.ndarray:
    """Enhances image details using Laplacian sharpening with configurable intensity."""
    kernel = np.array([[0, 1, 0],
                       [1, -4, 1],
                       [0, 1, 0]])
    
    laplacian_image = cv2.filter2D(src=image, ddepth=-1, kernel=kernel)
    return image + sharpening_factor * laplacian_image

def images_sr(image: np.ndarray, scaling_factor: int = 2) -> np.ndarray:
    sr_model = cv2.dnn_superres.DnnSuperResImpl_create()
    model_path = f"models/EDSR_x{scaling_factor}.pb"
    sr_model.readModel(model_path)
    sr_model.setModel("edsr", scaling_factor)
    scaled_image = sr_model.upsample(image)
    return scaled_image
