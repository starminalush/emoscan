import asyncio
import tempfile
import uuid
from base64 import b64encode
from itertools import chain, islice
from pathlib import Path

import httpx
from fastapi import APIRouter, UploadFile, File
import os
from loguru import logger

from utils import ImageConverter, extract_frames_from_video

router = APIRouter()


async def recognize(img_bytes):
    try:
        async with httpx.AsyncClient() as client:
            body = {
                "img_bytes": img_bytes
            }
            response = await client.post(url=os.getenv("MODEL_DEPLOYMENT_URI"), json=body)
            return response.json()
    except Exception as err:
        logger.error(err)
        return {}

def clean_result(emotion_recognition_result):
    return [item for item in [item for sublist in emotion_recognition_result for item in sublist] if item and item["emotion"] != "undefined emotion"]


@router.post('/')
async def upload_file(
        file: UploadFile = File(..., content_type=["image/jpeg", "image/png", "video/mp4", "video/x-msvideo"])):
    def chunks(iterable, size=10):
        iterator = iter(iterable)
        for first in iterator:
            yield chain([first], islice(iterator, size - 1))

    task_id  = uuid.uuid4()

    if file.content_type in ["video/mp4", "video/x-msvideo"]:
        video_recognition_results = []
        with tempfile.NamedTemporaryFile(suffix=Path(file.filename).suffix, delete=False) as temp_file:
            temp_file.write(await file.read())
            frames_generator = extract_frames_from_video(temp_file.name, n=5)

            for n, chunk in enumerate(chunks(frames_generator, 10)):
                # todo: реализовать на стороне сервиса с моделями возможность обработки по батчам
                frames = [ImageConverter.pil_to_base64(frame) for frame in list(chunk)]
                recognition_tasks = [recognize(frame) for frame in frames]
                recognition_result = await asyncio.gather(*recognition_tasks)
                video_recognition_results.extend(clean_result(recognition_result))
        return video_recognition_results
    else:
        return clean_result(await recognize(b64encode((file.file.read())).decode("utf-8")))
