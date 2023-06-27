from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.db.models import Event


async def get_all_students(
    db: AsyncSession,
):
    sql_statement = select(Event.track_id).distinct(Event.track_id)
    student_track_id_list = (await db.execute(sql_statement)).scalars().all()
    return student_track_id_list if student_track_id_list else []
