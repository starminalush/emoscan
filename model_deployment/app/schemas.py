from pydantic import BaseModel


class FaceBbox(BaseModel):
    x: int
    y: int
    x1: int
    y1: int


class Image(BaseModel):
    img_bytes: str
