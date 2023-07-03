from datetime import date

from pydantic.dataclasses import dataclass


@dataclass
class EmotionRecognitionResult:
    bbox: list[int]
    emotion: str
    track_id: int


@dataclass
class Analytics:
    emotion: str
    count: int
    date: date


class Student:
    track_id: int
