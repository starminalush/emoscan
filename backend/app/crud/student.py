from sqlalchemy import select, distinct
from sqlalchemy.ext.asyncio import AsyncSession

from core.db.models import Event


async def get_all_students(db: AsyncSession, start_index: int, limit: int):
    # идем в базу, выгружаем всех студентов по первой записи, берем их фотку из s3
    sql_statement = (
        (
            select(Event.track_id, Event.image_uuid, Event.datetime, Event.task_id, Event.bbox)
            .distinct(Event.track_id)
            .order_by(Event.track_id, Event.datetime)
        )
        .offset(start_index)
        .limit(limit)
    )
    result = (await db.execute(sql_statement)).fetchall()
    if result:
        return [res._asdict() for res in result]
    return []
