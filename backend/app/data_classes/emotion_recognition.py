from dataclasses import dataclass
from uuid import UUID
from datetime import datetime


@dataclass
class EmotionRecognitionHistoryEvent:
    task_id: UUID
    emotion: str
    bbox: list[int]
    track_id: int
    datetime: datetime
    image_uuid: UUID
    frame_number: int | None
