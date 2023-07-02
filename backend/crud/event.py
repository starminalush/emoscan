from dataclasses import asdict

from core.db.models import Event
from sqlalchemy.ext.asyncio import AsyncSession


async def add_recognition_event_to_db(
    db: AsyncSession,
    event_list,
):
    events_db = [Event(**asdict(event)) for event in event_list]
    db.add_all(events_db)
    await db.commit()
