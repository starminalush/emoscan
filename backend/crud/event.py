from dataclasses import asdict

from sqlalchemy.ext.asyncio import AsyncSession

from core.db.models import Event
from data_classes.emotion_recognition import EmotionRecognitionHistoryEvent


async def add_recognition_event_to_db(
    db: AsyncSession,
    event_list: list[EmotionRecognitionHistoryEvent],
):
    events_db = [Event(**asdict(event)) for event in event_list]
    db.add_all(events_db)
    await db.commit()
