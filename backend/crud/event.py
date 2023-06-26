from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from core.db.models import Event
from data_classes.emotion_recognition import EmotionRecognitionHistoryEvent


async def write_logs(db: AsyncSession, event: dict[str, Any]):
    event_db = Event(**event)
    db.add(event_db)
