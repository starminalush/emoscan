from fastapi import APIRouter

from api.endpoints import analytics, recognition, student


router = APIRouter()

router.include_router(recognition.router, prefix="/recognize", tags=["recognition"])
router.include_router(analytics.router, prefix="/analytics", tags=["analytics"])
router.include_router(student.router, prefix="/student", tags=["students"])
