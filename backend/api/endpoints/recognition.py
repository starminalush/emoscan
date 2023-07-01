import asyncio
import os
import tempfile
from collections import Counter
from datetime import datetime
from pathlib import Path
from uuid import UUID, uuid4

import httpx
from fastapi import APIRouter, Depends, File, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from api.deps import get_c3_client, get_db
from crud.event import write_logs
from data_classes.emotion_recognition import EmotionRecognitionHistoryEvent
from schemas.emotion_recognition import (
    EmotionRecognitionResponse,
    EmotionRecognitionResponseImage,
    EmotionRecognitionResponseVideo,
)
from utils.converters import cnvt_image_to_base64, cnvt_image_to_bytes
from utils.utils import chunks
from utils.video_frame_extractor import extract_frames_from_video

router = APIRouter()


async def recognize(img_bytes) -> list[EmotionRecognitionResponse | None]:
    try:
        async with httpx.AsyncClient() as client:
            body = {"img_bytes": cnvt_image_to_base64(img_bytes)}
            response = await client.post(
                url=os.getenv("MODEL_DEPLOYMENT_URI"), json=body
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
        await write_logs(db=db, event_list=events)

        image_path = (
            f"{current_date.strftime('%Y-%m-%d')}/{str(task_id)}/{image_uuid}.jpg"
        )
        await s3_client.upload_file(
             image_path, img_bytes
        )

        return [
            EmotionRecognitionResponseImage(
                bbox=emotion_recognition_result["bbox"],
                emotion=emotion_recognition_result["emotion"],
            )
            for emotion_recognition_result in emotion_recognition_results
        ]
    return []


@router.post("/image", response_model=list[EmotionRecognitionResponseImage])
async def upload_image(
    upload_file: UploadFile = File(
        ..., content_type=["image/jpeg", "image/png", "image/jpg"]
    ),
    db: AsyncSession = Depends(get_db),
    s3_client=Depends(get_c3_client),
):
    """Recognize emotions on faces in image file."""
    task_id: UUID = uuid4()
    return await process_frame_pipeline(
        img_bytes=(await upload_file.read()),
        task_id=task_id,
        db=db,
        s3_client=s3_client,
    )


@router.post("/video", response_model=EmotionRecognitionResponseVideo)
async def upload_video(
    upload_file: UploadFile = File(..., content_type=["video/mp4", "video/x-msvideo"]),
    db: AsyncSession = Depends(get_db),
    s3_client=Depends(get_c3_client),
):
    """Recognize emotions on faces in video file and return emotion statistics for uploaded video."""
    task_id: UUID = uuid4()
    counter = Counter()
    with tempfile.NamedTemporaryFile(
        suffix=Path(upload_file.filename).suffix, delete=False
    ) as temp_video_file:
        temp_video_file.write(await upload_file.read())
    frames_generator = extract_frames_from_video(temp_video_file.name, n=5)
    for idx_chunk, chunk in enumerate(chunks(frames_generator, 10)):
        frames = list(chunk)
        recognition_tasks = [
            process_frame_pipeline(
                db=db,
                img_bytes=cnvt_image_to_base64(frame),
                task_id=task_id,
                s3_client=s3_client,
                frame_number=(idx_chunk * 5 * 10) + (5 * idx_frame),
            )
            for idx_frame, frame in enumerate(frames, 1)
        ]
        recognition_results = await asyncio.gather(*recognition_tasks)
        recognition_results = [
            recognition_result
            for sublist in recognition_results
            for recognition_result in sublist
        ]
        counter.update(
            [recognition_result.emotion for recognition_result in recognition_results]
        )
    if counter.total() > 0:
        emotion_percentages = {
            emotion: count / counter.total() * 100 for emotion, count in counter.items()
        }
        return EmotionRecognitionResponseVideo(
            task_id=str(task_id), emotion_proportion=emotion_percentages
        )
    return {}
