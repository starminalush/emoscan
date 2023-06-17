import asyncio
import base64
import json
import shutil

import cv2
import httpx
from fastapi import APIRouter, UploadFile, File
import os
from loguru import logger

from utils import extract_frames

router = APIRouter()


async def recognize(img_bytes):
    try:
        async with httpx.AsyncClient() as client:
            body = {
                "img_bytes": img_bytes
            }
            response  = await client.post(url=os.getenv("MODEL_DEPLOYMENT_URI"), json=body)
            return response.json()
    except Exception as err:
        logger.error(err)
        return None


def save_base64_image(base64_string, file_path):
    # Декодирование строки Base64 в байтовую строку
    image_bytes = base64.b64decode(base64_string)

    # Сохранение изображения в файл
    with open(file_path, 'wb') as file:
        file.write(image_bytes)

def np_to_base64(np_array):
    # Кодирование изображения в формат Base64

    _, image_base64 = cv2.imencode('.png', np_array)
    return base64.b64encode(image_base64).decode('utf-8')

def bytes_to_base64(file_content):
    return base64.b64encode(file_content).decode("utf-8")

from itertools import chain, islice


def chunks(iterable, size=10):
    iterator = iter(iterable)
    for first in iterator:
        yield chain([first], islice(iterator, size - 1))


@router.post('/')
async def upload_file(file: UploadFile = File(..., content_type=["image/jpeg", "image/png", "video/mp4", "video/x-msvideo"])):
    "make it simple and stupid api"
    bucket_name = os.getenv("BUCKET_NAME")

    if file.content_type in ["video/mp4", "video/x-msvideo"]:
        #считываем каждый 5 кадр с видео
        with open(file.filename, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        frames_generator = extract_frames(file.filename, n=10)
        video_recognition_results = []
        count = 0
        for n, chunk in enumerate(chunks(frames_generator, 10)):
            frames = [np_to_base64(frame) for frame in list(chunk)]
            recognition_tasks = [recognize(frame) for frame in frames]

            recognition_result = await asyncio.gather(*recognition_tasks)
            logger.error(recognition_result)
            video_recognition_results.extend(recognition_result)
        return video_recognition_results
    else:
        #просто файл отправляем

        return await recognize(bytes_to_base64(file.file.read()))

























