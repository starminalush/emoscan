import cv2
import numpy as np


def cnvt_bytes_to_numpy(image: bytes) -> np.ndarray:
    np_array = np.frombuffer(image, np.uint8)
    return cv2.imdecode(np_array, cv2.IMREAD_COLOR)
