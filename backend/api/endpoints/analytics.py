from datetime import date

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from api.deps import get_db
from crud.analytics import get_analytics_by_range_of_dates, get_analytics_by_student_id
from schemas.analytics import AnalyticsByRangeOfDates

router = APIRouter()


@router.get("/", response_model=list[AnalyticsByRangeOfDates | None])
async def get_analytics_by_dates(
    date_start: date = Query(...), date_end: date = Query(...), db: AsyncSession = Depends(get_db)
):
    """Get analytics by all students by range of dates.

    Args:
        date_start: Range start date.
        date_end:  Range end date incl.
        db: SQLAlchemy local session.

    Returns:
        List of AnalyticsByRangeOfDates each containing emotion, emotion's count and date.
    """
    return await get_analytics_by_range_of_dates(
        db=db, date_start=date_start, date_end=date_end
    )


@router.get("/{student_track_id}", response_model=list[AnalyticsByRangeOfDates | None])
async def get_analytics_by_student(
    student_track_id: int,
    date_start: date = Query(...),
    date_end: date = Query(...),
    db: AsyncSession = Depends(get_db),
):
    """Get analytics by student's track id and range of dates.

    Args:
        student_track_id: Student's track ID.
        date_start: Range date start.
        date_end: Range date end.
        db: SQLAlchemy local session,

    Returns:
        List of AnalyticsByRangeOfDates each containing emotion, emotion's count and date.
    """
    return await get_analytics_by_student_id(
        db=db, student_track_id=student_track_id, start_date=date_start, end_date=date_end
    )
