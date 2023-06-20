import asyncio
import base64
import tempfile
import uuid
from datetime import datetime
from io import BytesIO

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
from api.deps import get_db, get_c3_client
from schemas.emotion_detection import EmotionDetectionResponse


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


async def process_frame(db: AsyncSession, img_bytes, task_id, s3_client):
    recognition_result = await recognize(img_bytes)
    image_uuid = uuid.uuid4()
    current_date = datetime.today()
    result = []
    for res in recognition_result:
        history_data = {
            "task_id": task_id,
            "emotion": res['emotion'],
            "bbox": res["bbox"],
            "track_id": res["track_id"],
            "image_uuid": image_uuid,
            "datetime": current_date
        }
        await write_logs(db, history_data)

        result.append(EmotionDetectionResponse(bbox=res["bbox"], emotion=res["emotion"]))

    image_path = f"{current_date.strftime('%Y-%m-%d')}/{str(task_id)}/{image_uuid}.jpg"
    image_bytes = base64.b64decode(img_bytes)
    await s3_client.upload_fileobj(BytesIO(image_bytes), "logs",  image_path)
    return result

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
        s3_client=Depends(get_c3_client)
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
                #тут мы ничего не возврашаем, тут копим результаты и пишем видео назад

    else:
        return await process_frame(db,
                            b64encode((await file.read())).decode("utf-8"),
                            task_id,
                            s3_client
                            )
