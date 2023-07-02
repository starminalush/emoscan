from base64 import b64encode


def cnvt_image_to_base64(image: bytes):
    return b64encode(image).decode("utf-8")
