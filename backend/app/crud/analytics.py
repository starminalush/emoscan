from sqlalchemy import select, func

from core.db.models import History
from sqlalchemy.ext.asyncio import AsyncSession


async def get_stats_by_date(db:AsyncSession, date:str):
    sql_statement = select(History).where(func.to_char(History.datetime, '%Y-%m-%d') == date)

    return await db.execute(sql_statement).scalars().all()


async def get_stats_by_student(db:AsyncSession, student_id: int):
    sql_statement = select(History).where(History.track_id == student_id)
    return await db.execute(sql_statement).scalars().all()

