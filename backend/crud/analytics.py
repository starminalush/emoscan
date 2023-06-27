from datetime import date

from sqlalchemy import Date, cast, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from core.db.models import Event
from schemas.analytics import AnalyticsByRangeOfDates, AnalyticsByStudentID


async def get_analytics_by_range_of_dates(
    db: AsyncSession, date_start: date, date_end: date
) -> list[AnalyticsByRangeOfDates | None]:
    sql_statement = (
        select(cast(Event.datetime, Date), Event.emotion, func.count(Event.emotion))
        .where(cast(Event.datetime, Date).between(date_start, date_end))
        .group_by(cast(Event.datetime, Date), Event.emotion)
    )

    analytics_by_date = (await db.execute(sql_statement)).scalars().all()
    return analytics_by_date if analytics_by_date else []


async def get_analytics_by_student_id(
    db: AsyncSession, student_id: int, start_date: date, end_date: date
) -> list[AnalyticsByStudentID | None]:
    sql_statement = (
        select(Event.emotion, func.count(Event.emotion), cast(Event.datetime, Date))
        .where(
            Event.track_id == student_id,
            cast(Event.datetime, Date).between(start_date, end_date),
        )
        .group_by(cast(Event.datetime, Date), Event.emotion)
    )
    statistics_by_student = (await db.execute(sql_statement)).scalars().all()

    return statistics_by_student if statistics_by_student else []
