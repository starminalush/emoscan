from datetime import date, datetime

from sqlalchemy import select, func, cast, Date

from core.db.models import Event
from sqlalchemy.ext.asyncio import AsyncSession


async def get_stats_by_range_of_date(
    db: AsyncSession, start_date: datetime, end_date: datetime
):
    sql_statement = (
        select(cast(Event.datetime, Date), Event.emotion, func.count(Event.emotion))
        .where(Event.datetime.between(start_date, end_date))
        .group_by(cast(Event.datetime, Date), Event.emotion)
    )

    result = (await db.execute(sql_statement)).fetchall()
    if result:
        return [res._asdict() for res in result]
    else:
        return []


async def get_stats_by_student_id(db: AsyncSession, student_id: int):
    sql_statement = select(Event).where(Event.track_id == student_id)
    return await db.execute(sql_statement).scalars().all()
