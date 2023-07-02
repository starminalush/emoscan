from loguru import logger
import requests
from itertools import islice
from os import getenv
from PIL import Image


def recognize(image_bytes:bytes, task_id:str):
    files = {"upload_file": image_bytes}
    body = {"task_id": task_id}
    response = requests.post(f"{getenv('BACKEND_URI')}/recognize/", files=files, data=body)
    logger.error(response.content)
    if response.status_code == 200:
        return response.json()
    return []


def crop_face(bbox: list[int], image_file: bytes) -> Image:
    image = Image.open(image_file)
    return image.crop(bbox)

