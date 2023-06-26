from sqlalchemy import distinct, select
from sqlalchemy.ext.asyncio import AsyncSession

from core.db.models import Event


async def get_all_students(
    db: AsyncSession,
):
    sql_statement = select(Event.track_id).distinct(Event.track_id)
    result = (await db.execute(sql_statement)).fetchall()
    if result:
        return [res._asdict() for res in result]
    return []
