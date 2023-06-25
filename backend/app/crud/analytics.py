from datetime import date, datetime

from sqlalchemy import select, func, cast, Date

from core.db.models import Event
from sqlalchemy.ext.asyncio import AsyncSession


async def get_stats_by_range_of_date(
    db: AsyncSession, start_date: datetime, end_date: datetime
):
    sql_statement = (
        select(cast(Event.datetime, Date), Event.emotion, func.count(Event.emotion))
        .where(cast(Event.datetime, Date).between(start_date, end_date))
        .group_by(cast(Event.datetime, Date), Event.emotion)
    )

    result = (await db.execute(sql_statement)).fetchall()
    if result:
        return [res._asdict() for res in result]
    else:
        return []


async def get_stats_by_student_id(db: AsyncSession, student_id: int, start_date, end_date):
    sql_statement = select(Event.emotion, func.count(Event.emotion), cast(Event.datetime,  Date)).where(Event.track_id == student_id, cast(Event.datetime, Date).between(start_date, end_date)).group_by(cast(Event.datetime, Date), Event.emotion)
    result = (await db.execute(sql_statement)).fetchall()

    if result:
        return [res._asdict() for res in result]
    else:
         return []
