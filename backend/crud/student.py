from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.db.models import Event
from schemas.student import Student


async def get_all_students(
    db: AsyncSession,
) -> list[Student | None]:
    sql_statement = select(Event.track_id).distinct(Event.track_id)
    student_track_id_list = (await db.execute(sql_statement)).scalars().all()
    return [
        Student(track_id=student_track_id) for student_track_id in student_track_id_list
    ]
