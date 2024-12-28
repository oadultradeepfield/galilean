import numpy as np

from image_stacking.utils import (mean_image_stacking,
                                  mean_image_stacking_with_clipping,
                                  mean_image_stacking_with_median_clipping,
                                  median_image_stacking)


def image_stacking(images: np.ndarray, method: str = "mean_with_median_clipping") -> np.ndarray:
    """Stack and perform superresolution on images using the specified method."""
    method_map = {
        "mean": mean_image_stacking,
        "median": median_image_stacking,
        "mean_with_clipping": mean_image_stacking_with_clipping,
        "mean_with_median_clipping": mean_image_stacking_with_median_clipping
    }
    return method_map.get(method)(images)
