import requests
from PIL import Image


def recognize(image_bytes, uri) -> list[dict[str, str | list[int]] | dict]:
    files = {"file": image_bytes}
    response = requests.post(uri, files=files)
    if response.status_code == 200:
        return response.json()
    return []


def crop_face(bbox: list[int], image_file: bytes) -> Image:
    image = Image.open(image_file)
    return image.crop(bbox)
