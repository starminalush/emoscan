from fastapi import APIRouter
from api.endpoints import recognition, analytics

router = APIRouter()

router.include_router(recognition.router, prefix="/recognize", tags=["recognition"])
router.include_router(analytics.router, prefix="/analytics", tags=["analytics"])
