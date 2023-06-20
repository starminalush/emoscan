import asyncio
from collections import Counter
from loguru import logger
import os
import tempfile
from dataclasses import asdict
from datetime import datetime
from itertools import chain, islice
from pathlib import Path
from uuid import UUID, uuid4

import httpx
from fastapi import APIRouter, Depends, File, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from api.deps import get_c3_client, get_db
from crud.event import write_logs
from data_classes import EmotionRecognitionHistoryEvent
from schemas.emotion_detection import (
    EmotionRecognitionResponse,
    EmotionRecognitionResponseImage,
    EmotionRecognitionResponseVideo,
)
from utils.converters import cnvt_image_to_base64, cnvt_image_to_bytes
from utils.video_frame_extractor import extract_frames_from_video

router = APIRouter()


async def recognize(img_bytes) -> list[EmotionRecognitionResponse | None]:
    try:
        async with httpx.AsyncClient() as client:
            body = {"img_bytes": img_bytes}
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
    logger.error(emotion_recognition_results)
    if emotion_recognition_results:
        image_uuid: UUID = uuid4()
        current_date: datetime = datetime.today()
        for result in emotion_recognition_results:
            event = EmotionRecognitionHistoryEvent(
                task_id=task_id,
                emotion=result["emotion"],
                bbox=result["bbox"],
                track_id=result["track_id"],
                image_uuid=image_uuid,
                datetime=current_date,
                frame_number=frame_number,
            )
            await write_logs(db=db, event=asdict(event))

        image_path = (
            f"{current_date.strftime('%Y-%m-%d')}/{str(task_id)}/{image_uuid}.jpg"
        )
        await s3_client.upload_fileobj(
            cnvt_image_to_bytes(img_bytes), "logs", image_path
        )

        return [
            EmotionRecognitionResponseImage(bbox=item["bbox"], emotion=item["emotion"])
            for item in emotion_recognition_results
        ]
    return []


@router.post("/image", response_model=list[EmotionRecognitionResponseImage])
async def upload_image(
    file: UploadFile = File(..., content_type=["image/jpeg", "image/png", "image/jpg"]),
    db: AsyncSession = Depends(get_db),
    s3_client=Depends(get_c3_client),
):
    task_id: UUID = uuid4()
    result = await process_frame_pipeline(
        img_bytes=cnvt_image_to_base64((await file.read())),
        task_id=task_id,
        db=db,
        s3_client=s3_client,
    )
    await db.commit()
    return result


@router.post("/video", response_model=EmotionRecognitionResponseVideo)
async def upload_video(
    file: UploadFile = File(..., content_type=["video/mp4", "video/x-msvideo"]),
    db: AsyncSession = Depends(get_db),
    s3_client=Depends(get_c3_client),
):
    def chunks(iterable, size=10):
        iterator = iter(iterable)
        for first in iterator:
            yield chain([first], islice(iterator, size - 1))

    task_id: UUID = uuid4()
    counter = Counter()
    with tempfile.NamedTemporaryFile(
        suffix=Path(file.filename).suffix, delete=False
    ) as temp_file:
        temp_file.write(await file.read())
    # для увеличения скорости обработки видео - берем каждый 5 кадр. Отправляем запросы на сервис распознавания пачкой тасок
    frames_generator = extract_frames_from_video(temp_file.name, n=5)
    for n, chunk in enumerate(chunks(frames_generator, 10)):
        initial_frames = list(chunk)
        frames = [frame for frame in initial_frames]
        recognition_tasks = [
            process_frame_pipeline(
                db=db,
                img_bytes=cnvt_image_to_base64(frame),
                task_id=task_id,
                s3_client=s3_client,
                frame_number=(n * 5 * 10) + (5 * idx),
            )
            for idx, frame in enumerate(frames, 1)
        ]
        recognition_results = await asyncio.gather(*recognition_tasks)
        recognition_results = [
            item for sublist in recognition_results for item in sublist
        ]
        counter.update([data.emotion for data in recognition_results])
    if counter.total() > 0:
        emotion_percentages = {
            item: count / counter.total() * 100 for item, count in counter.items()
        }
        return EmotionRecognitionResponseVideo(
            task_id=str(task_id), emotion_proportion=emotion_percentages
        )
    return {}
