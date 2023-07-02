from datetime import date

from api.deps import get_db
from crud.analytics import get_analytics_by_range_of_dates, get_analytics_by_student_id
from fastapi import APIRouter, Depends, Query
from schemas.analytics import AnalyticsByRangeOfDates

router = APIRouter()


@router.get("/", response_model=list[AnalyticsByRangeOfDates | None])
async def get_analytics_by_date(
    date_start: date = Query(...), date_end: date = Query(...), db=Depends(get_db)
):
    return await get_analytics_by_range_of_dates(
        db=db, date_start=date_start, date_end=date_end
    )


@router.get("/{student_id}", response_model=list[AnalyticsByRangeOfDates | None])
async def get_analytics_by_student(
    student_id: int,
    date_start: date = Query(...),
    date_end: date = Query(...),
    db=Depends(get_db),
):
    return await get_analytics_by_student_id(
        db=db, student_id=student_id, start_date=date_start, end_date=date_end
    )
