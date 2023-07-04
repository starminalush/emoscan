from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api.deps import get_db
from crud.student import get_all_students
from schemas.student import Student

router = APIRouter()


@router.get("/", response_model=list[Student | None])
async def get_students(db: AsyncSession = Depends(get_db)):
    """Get all students' track ids from db for all time.

    Args:
        db: SQLAlchemy local session.

    Returns:
        List of Student each containing track_id.
    """
    return await get_all_students(db=db)
