from sqlalchemy import select, distinct
from sqlalchemy.ext.asyncio import AsyncSession

from core.db.models import Event


async def get_all_students(db: AsyncSession,):
    # идем в базу, выгружаем всех студентов по первой записи, берем их фотку из s3
    sql_statement = (
        (
            select(Event.track_id)
            .distinct(Event.track_id)
        )
    )
    result = (await db.execute(sql_statement)).fetchall()
    if result:
        return [res._asdict() for res in result]
    return []
