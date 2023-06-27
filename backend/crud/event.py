from dataclasses import asdict

from sqlalchemy.ext.asyncio import AsyncSession

from core.db.models import Event
from data_classes.emotion_recognition import EmotionRecognitionHistoryEvent


async def write_logs(
    db: AsyncSession,
    event_list: EmotionRecognitionHistoryEvent | list[EmotionRecognitionHistoryEvent],
):
    if isinstance(event_list, list):
        events_db = [Event(**asdict(event)) for event in event_list]
        db.add_all(events_db)
    else:
        event_db = Event(**asdict(event_list))
        db.add(event_db)
    await db.commit()
