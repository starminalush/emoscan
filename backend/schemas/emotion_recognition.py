from pydantic import BaseModel


class EmotionRecognitionResponseImage(BaseModel):
    bbox: list[int]
    emotion: str


class EmotionRecognitionResponse(EmotionRecognitionResponseImage):
    track_id: int


class EmotionRecognitionResponseVideo(BaseModel):
    task_id: str
    emotion_proportion: dict[str, float]


class EmotionRecognitionRequestData(BaseModel):
    task_id: str
