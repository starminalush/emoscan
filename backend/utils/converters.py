from base64 import b64encode, b64decode
from io import BytesIO
from PIL.Image import Image
from functools import singledispatch


@singledispatch
def cnvt_image_to_base64(image):
    return image


@cnvt_image_to_base64.register
def _(image: bytes):
    return b64encode(image).decode("utf-8")


@cnvt_image_to_base64.register
def _(image: Image):
    buffered = BytesIO()
    image.save(buffered, format="JPEG")
    return b64encode(buffered.getvalue()).decode("utf-8")


def cnvt_image_to_bytes(image: str):
    return BytesIO(b64decode(image))
