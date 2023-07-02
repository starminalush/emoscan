from api.deps import get_db
from crud.student import get_all_students
from fastapi import APIRouter, Depends
from schemas.student import Student
from sqlalchemy.ext.asyncio import AsyncSession
router = APIRouter()


@router.get("/", response_model=list[Student | None])
async def get_students(db: AsyncSession = Depends(get_db)):
    return await get_all_students(db=db)
