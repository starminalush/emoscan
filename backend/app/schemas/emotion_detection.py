from pydantic import BaseModel


class EmotionDetectionResponse(BaseModel):
    img_bytes: str
    emotion: str
