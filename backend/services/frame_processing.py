from datetime import datetime
from os import getenv
from uuid import UUID, uuid4

from loguru import logger

import httpx
from crud.event import add_recognition_event_to_db
from data_classes.emotion_recognition import EmotionRecognitionHistoryEvent
from schemas.emotion_recognition import EmotionRecognitionResponse
from sqlalchemy.ext.asyncio import AsyncSession


async def recognize(img_bytes) -> list[EmotionRecognitionResponse | None]:
    try:
        async with httpx.AsyncClient() as client:
            body = {"base64_image": img_bytes}
            response = await client.post(url=getenv("MODEL_DEPLOYMENT_URI"), json=body)
            return response.json()
    except Exception:
        return []


def _create_event(recognition_result, image_uuid, current_date, task_id) -> EmotionRecognitionHistoryEvent:
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
    emotion_recognition_results: list,
    db: AsyncSession,
    s3_client,
    img_bytes,
):
    image_uuid: UUID = uuid4()
    current_date: datetime = datetime.today()
    upload_id = None
    image_path = f"{current_date.strftime('%Y-%m-%d')}/{str(task_id)}/{image_uuid}.jpg"
    try:
        events_list: list[EmotionRecognitionHistoryEvent] = [
            _create_event(emotion_data, image_uuid, current_date, task_id)
            for emotion_data in emotion_recognition_results
        ]
        await add_recognition_event_to_db(db=db, event_list=events_list)
        upload_id = await s3_client.upload_file(
            image_path, img_bytes
        )
    except Exception as err:
        logger.error(err)
        if upload_id:
            await s3_client.abort_file_upload(filename=image_path, upload_id=upload_id)
        await db.rollback()

