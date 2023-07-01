from os import getenv
from uuid import UUID

import httpx

from schemas.emotion_recognition import EmotionRecognitionResponse


async def recognize(img_bytes) -> list[EmotionRecognitionResponse | None]:
    try:
        async with httpx.AsyncClient() as client:
            body = {"img_bytes": img_bytes}
            response = await client.post(
                url=getenv("MODEL_DEPLOYMENT_URI"), json=body
            )
            return response.json()
    except Exception:
        return []


async def process_frame_pipeline(
    img_bytes: str, task_id: UUID, db: AsyncSession, s3_client, frame_number=None
):
    emotion_recognition_results: list[
        EmotionRecognitionResponse | None
    ] = await recognize(img_bytes=img_bytes)
    if emotion_recognition_results:
        image_uuid: UUID = uuid4()
        current_date: datetime = datetime.today()
        events = [
            EmotionRecognitionHistoryEvent(
                task_id=task_id,
                emotion=emotion_recognition_result["emotion"],
                bbox=emotion_recognition_result["bbox"],
                track_id=emotion_recognition_result["track_id"],
                image_uuid=image_uuid,
                datetime=current_date,
                frame_number=frame_number,
            )
            for emotion_recognition_result in emotion_recognition_results
        ]
        # await write_logs(db=db, event_list=events)
        #
        # image_path = (
        #     f"{current_date.strftime('%Y-%m-%d')}/{str(task_id)}/{image_uuid}.jpg"
        # )
        # await s3_client.upload_fileobj(
        #     cnvt_image_to_bytes(img_bytes), "logs", image_path
        # )

        return [
            EmotionRecognitionResponseImage(
                bbox=emotion_recognition_result["bbox"],
                emotion=emotion_recognition_result["emotion"],
            )
            for emotion_recognition_result in emotion_recognition_results
        ]
    return []