from pydantic import BaseModel


class EmotionRecognitionResponse(BaseModel):
    bbox: list[int]
    emotion: str


class EmotionRecognitionResponseFull(EmotionRecognitionResponse):
    track_id: int
