from base64 import b64encode


def cnvt_image_to_base64(image: bytes):
    """Convert image bytes to base64 string.
    Args:
        image: Image bytes.

    Returns:
        Base64 image string.
    """
    return b64encode(image).decode("utf-8")
