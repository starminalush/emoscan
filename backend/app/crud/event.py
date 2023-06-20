from typing import Any

from core.db.models import Event
from sqlalchemy.ext.asyncio import AsyncSession
from data_classes import EmotionRecognitionHistoryEvent


async def write_logs(db: AsyncSession, event: dict[str, Any]):
    event_db = Event(**event)
    db.add(event_db)
    await db.commit()
