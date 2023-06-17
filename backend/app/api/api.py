from fastapi import APIRouter
from api.endpoints import recognition
router = APIRouter()

router.include_router(recognition.router, prefix="/recognize", tags=["recognition"])