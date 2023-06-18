from base64 import b64decode, b64encode
from io import BytesIO

from PIL import Image


class ImageConverter:
    @staticmethod
    def base64_to_pil(image: bytes | str) -> Image:
        binary_data = b64decode(image)
        return Image.open(BytesIO(binary_data))

    @staticmethod
    def bbox_to_string(bbox: list[int | float]) -> str:
        return ",".join(map(str, bbox))

    @staticmethod
    def string_to_bbox(string_bbox: str) -> list[int]:
        return list(map(int, string_bbox.split(",")))

    @staticmethod
    def pil_to_base64(image: Image) -> str:
        buffered = BytesIO()
        image.save(buffered, format="JPEG")
        return b64encode(buffered.getvalue()).decode("utf-8")