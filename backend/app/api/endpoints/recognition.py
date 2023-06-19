import asyncio
import tempfile
import uuid
from datetime import datetime
from PIL import Image
from base64 import b64encode
from itertools import chain, islice
from pathlib import Path

import httpx
from fastapi import APIRouter, UploadFile, File, Depends
import os
from loguru import logger
from crud.history import write_logs
from sqlalchemy.ext.asyncio import AsyncSession
from utils import ImageConverter, extract_frames_from_video
from api.deps import get_db, get_s3_client

from backend.core.minio.s3_client import S3Client

router = APIRouter()


async def recognize(img_bytes):
    try:
        async with httpx.AsyncClient() as client:
            body = {"img_bytes": img_bytes}
            response = await client.post(
                url=os.getenv("MODEL_DEPLOYMENT_URI"), json=body
            )
            return response.json()
    except Exception as err:
        logger.error(err)
        return {}


async def process_frame(db: AsyncSession, img_bytes, task_id, s3_client: S3Client):
    recognition_result = await recognize(img_bytes)

    image_uuid = uuid.uuid4()
    current_date = datetime.today().strftime('%Y-%m-%d')

    history_data = {
        "task_id": task_id,
        "emotion": recognition_result['emotion'],
        "bbox": recognition_result["bbox"],
        "track_id": recognition_result["track_id"],
        "image_uuid": image_uuid,
        "datetime": current_date
    }
    await write_logs(db, **history_data)

    image_path = f"{current_date}/{str(task_id)}/{image_uuid}.jpg"
    await s3_client.write_image(image_bytes=img_bytes, image_path=image_path)


def crop_face_from_image(frame: Image, bbox):
    return frame.crop(box=bbox)


def clean_result(emotion_recognition_result):
    return [
        item
        for item in emotion_recognition_result
        if item
    ]


@router.post("/")
async def upload_file(
        file: UploadFile = File(
            ..., content_type=["image/jpeg", "image/png", "video/mp4", "video/x-msvideo"]
        ),
        db=Depends(get_db),
        s3_client=Depends(get_s3_client)
):
    def chunks(iterable, size=10):
        iterator = iter(iterable)
        for first in iterator:
            yield chain([first], islice(iterator, size - 1))

    task_id = uuid.uuid4()
    if file.content_type in ["video/mp4", "video/x-msvideo"]:
        with tempfile.NamedTemporaryFile(
                suffix=Path(file.filename).suffix, delete=False
        ) as temp_file:
            temp_file.write(await file.read())
            frames_generator = extract_frames_from_video(temp_file.name, n=5)

            for n, chunk in enumerate(chunks(frames_generator, 10)):
                # todo: реализовать на стороне сервиса с моделями возможность обработки по батчам
                initial_frames = list(chunk)
                frames = [ImageConverter.pil_to_base64(frame) for frame in initial_frames]
                recognition_tasks = [process_frame(db, frame, task_id, s3_client) for frame in frames]
                _ = await asyncio.gather(*recognition_tasks)

    else:
        await process_frame(db,
                            b64encode((await file.read())).decode("utf-8"),
                            task_id,
                            s3_client
                            )
