from fastapi import APIRouter

from api.endpoints import recognition, analytics, students

router = APIRouter()

router.include_router(recognition.router, prefix="/recognize", tags=["recognition"])
router.include_router(analytics.router, prefix="/analytics", tags=["analytics"])
router.include_router(students.router, prefix="/students", tags=["students"])
