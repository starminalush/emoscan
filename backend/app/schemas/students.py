from pydantic import BaseModel


class Student(BaseModel):
    track_id: int
