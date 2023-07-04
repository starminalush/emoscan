from pydantic import BaseModel

from aliases import DetectionBbox


class TrackerResult(BaseModel):
    bbox: DetectionBbox
    track_id: int


class RecognitionResult(TrackerResult):
    emotion: str
