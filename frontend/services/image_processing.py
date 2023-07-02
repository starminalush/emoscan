from PIL import Image


def crop_face(bbox: list[int], image_file: bytes) -> Image:
    image = Image.open(image_file)
    return image.crop(bbox)
