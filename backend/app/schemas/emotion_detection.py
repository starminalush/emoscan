from pydantic import BaseModel


class EmotionDetectionResponse(BaseModel):
    bbox: list[int]
    emotion: str
