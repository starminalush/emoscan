from pydantic import BaseModel

from aliases import DetectionBbox


class Image(BaseModel):
    img_bytes: str


class TrackerResult(BaseModel):
    bbox: DetectionBbox
    track_id: int


class RecognitionResult(TrackerResult):
    emotion: str
