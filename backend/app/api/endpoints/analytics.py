from fastapi import APIRouter, Depends, Query
from datetime import date
from api.deps import get_db
from crud.analytics import get_stats_by_range_of_date, get_stats_by_student_id
from schemas.analytics import AnalyticsPerRangeOfDates

router = APIRouter()


@router.get("/dates", response_model=list[AnalyticsPerRangeOfDates | None])
async def get_analytics_by_date(
    date_start: date = Query(...), date_end: date = Query(...), db=Depends(get_db)
):
    result = await get_stats_by_range_of_date(
        db=db, start_date=date_start, end_date=date_end
    )
    return result if result else []


@router.get("/{student_id}")
async def get_analytics_by_student(student_id: int,   date_start: date = Query(...), date_end: date = Query(...), db=Depends(get_db)):
    return await get_stats_by_student_id(db=db, student_id=student_id, start_date=date_start, end_date=date_end)
