from base64 import b64encode


def cnvt_bytes_to_base64(img_bytes: bytes):
    return b64encode(img_bytes).decode("utf-8")
