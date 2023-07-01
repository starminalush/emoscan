from pydantic import BaseModel

from aliases import DetectionBbox


class Image(BaseModel):
    base64_image: str


class TrackerResult(BaseModel):
    bbox: DetectionBbox
    track_id: int


class RecognitionResult(TrackerResult):
    emotion: str
