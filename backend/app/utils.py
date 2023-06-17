import base64
from itertools import chain, islice

import cv2
import ffmpeg
import numpy as np
import av
from loguru import logger


def extract_frames(video_path, n):
    container = av.open(video_path)
    stream = container.streams.video[0]

    for frame in container.decode(stream):
        if frame.index % n == 0:
            opencv_image = frame.to_rgb().to_ndarray()
            yield opencv_image


def chunks(iterable, size=10):
    iterator = iter(iterable)
    for first in iterator:
        yield chain([first], islice(iterator, size - 1))


def bytes_to_base64(file_content):
    return base64.b64encode(file_content).decode("utf-8")


def np_to_base64(np_array):
    # Кодирование изображения в формат Base64

    _, image_base64 = cv2.imencode('.png', np_array)
    return base64.b64encode(image_base64).decode('utf-8')
