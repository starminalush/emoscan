from fastapi import APIRouter, Depends

from api.deps import get_db
from crud.analytics import get_stats_by_date, get_stats_by_student_id

router = APIRouter()


@router.get("/{date}")
async def get_analytics_by_date(date: str, db=Depends(get_db)):
    return await get_stats_by_date(db=db, date=date)


@router.get("/{student_id}")
async def get_analytics_by_student(student_id: str, db=Depends(get_db)):
    return await get_stats_by_student_id(db=db, student_id=student_id)
