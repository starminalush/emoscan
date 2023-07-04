from datetime import datetime, date
from os import getenv
from uuid import UUID, uuid4

import httpx
from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession

from core.s3.s3client import S3Client
from crud.event import add_recognition_event_to_db
from data_classes.emotion_recognition import EmotionRecognitionHistoryEvent
from schemas.emotion_recognition import EmotionRecognitionResponse


async def recognize(img_bytes: bytes) -> list[EmotionRecognitionResponse | None]:
    """Get recognition emotions on image.

    Args:
        img_bytes: Input image.

    Returns:
        List of EmotionRecognitionResponse each containing track_id, emotion and face bbox.
    """
    try:
        async with httpx.AsyncClient() as client:
            files = {"upload_file": img_bytes}
            response = await client.post(url=f"{getenv('MODEL_DEPLOYMENT_URI')}/predict/", files=files)
            return response.json()
    except Exception as err:
        logger.error(err)
        return []


def _create_event(
    recognition_result: EmotionRecognitionResponse, image_uuid: UUID, current_date: date, task_id: UUID
) -> EmotionRecognitionHistoryEvent:
    return EmotionRecognitionHistoryEvent(
        task_id=task_id,
        emotion=recognition_result["emotion"],
        bbox=recognition_result["bbox"],
        track_id=recognition_result["track_id"],
        image_uuid=image_uuid,
        datetime=current_date,
    )


async def write_logs(
    task_id: UUID,
    emotion_recognition_results: list[EmotionRecognitionResponse],
    db: AsyncSession,
    s3_client: S3Client,
    img_bytes: bytes,
):
    """Write recognition events to db and s3.

    Args:
        task_id: TaskID. Ex: lesson ID.
        emotion_recognition_results: List of emotion recogition results.
        db: SQLAlchemy local session.
        s3_client: S3Client object.
        img_bytes: Input image.
    """
    image_uuid: UUID = uuid4()
    current_date: datetime = datetime.today()
    image_path = f"{current_date.strftime('%Y-%m-%d')}/{str(task_id)}/{image_uuid}.jpg"
    try:
        events_list: list[EmotionRecognitionHistoryEvent] = [
            _create_event(emotion_data, image_uuid, current_date, task_id)
            for emotion_data in emotion_recognition_results
        ]
        await add_recognition_event_to_db(db=db, event_list=events_list)
        await s3_client.upload_file(filename=image_path, img_bytes=img_bytes)
    except Exception as err:
        logger.error(err)
        await db.rollback()
