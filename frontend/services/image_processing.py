from PIL import Image


def crop_face(bbox: list[int], image: bytes) -> Image:
    """Crop face from image.

    Args:
        bbox: Face bbox.
        image: Image with face.

    Returns:
        Cropped face from image.
    """
    return Image.open(image).crop(bbox)
