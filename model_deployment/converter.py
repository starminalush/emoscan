import base64

import cv2
import numpy as np


def cnvt_base64_to_numpy(image: str) -> np.ndarray:
    im_bytes = base64.b64decode(image)
    im_arr = np.frombuffer(im_bytes, dtype=np.uint8)
    return cv2.imdecode(im_arr, flags=cv2.IMREAD_COLOR)
