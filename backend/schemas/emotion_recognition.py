from pydantic import BaseModel


class EmotionRecognitionResponse(BaseModel):
    bbox: list[int]
    emotion: str
    track_id: int
