from base64 import b64decode
from pathlib import Path
from typing import TypeAlias

import cv2
import gdown as gdown
import numpy as np

FaceBbox: TypeAlias = list[int]


def load_image_into_numpy_array(data):
    binary_data = b64decode(data)
    return cv2.imdecode(np.frombuffer(binary_data, np.uint8), -1)
