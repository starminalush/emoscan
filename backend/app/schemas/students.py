from pydantic import BaseModel


class Student(BaseModel):
    track_id: int
    image_url: str
    bbox:list[int|float]
