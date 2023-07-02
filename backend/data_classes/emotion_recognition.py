from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass
class EmotionRecognitionHistoryEvent:
    task_id: UUID
    emotion: str
    bbox: list[int]
    track_id: int
    datetime: datetime
    image_uuid: UUID


