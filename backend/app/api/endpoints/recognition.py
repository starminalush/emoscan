import asyncio
import tempfile
from PIL import Image
from base64 import b64encode
from itertools import chain, islice
from pathlib import Path

import httpx
from fastapi import APIRouter, UploadFile, File
import os
from loguru import logger
from schemas.emotion_detection import EmotionDetectionResponse
from utils import ImageConverter, extract_frames_from_video

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


def crop_face_from_image(frame: Image, bbox):
    return frame.crop(box=bbox)


def clean_result(emotion_recognition_result):
    return [
        item
        for item in emotion_recognition_result
        if item
    ]


@router.post("/", response_model=list[EmotionDetectionResponse])
async def upload_file(
    file: UploadFile = File(
        ..., content_type=["image/jpeg", "image/png", "video/mp4", "video/x-msvideo"]
    )
):
    def chunks(iterable, size=10):
        iterator = iter(iterable)
        for first in iterator:
            yield chain([first], islice(iterator, size - 1))

    video_recognition_results = []
    crops = []
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
                recognition_tasks = [recognize(frame) for frame in frames]
                recognition_results = await asyncio.gather(*recognition_tasks)

                recognition_results = [
                    item for sublist in recognition_results for item in sublist
                ]
                video_recognition_results.extend(clean_result(recognition_results))
                for frame, recognized_result in zip(initial_frames, recognition_results):
                    logger.error(recognized_result)
                    if recognized_result:
                        crop_face = crop_face_from_image(
                            frame, recognized_result["bbox"]
                        )
                        crop_img_bytes = ImageConverter.pil_to_base64(crop_face)
                        crops.append(
                            EmotionDetectionResponse(
                                img_bytes=crop_img_bytes,
                                emotion=recognized_result["emotion"],
                            )
                        )
                        logger.error(recognized_result["emotion"])
    else:
        recognition_result = await recognize(
            b64encode((await file.read())).decode("utf-8")
        )
        logger.error(recognition_result)
        for result in recognition_result:
            if result:
                img = Image.open(file.file)
                crop_face = crop_face_from_image(img, result["bbox"])
                crop_img_bytes = ImageConverter.pil_to_base64(crop_face)
                crops.append(
                    EmotionDetectionResponse(
                        img_bytes=crop_img_bytes, emotion=result["emotion"]
                    )
                )

    return crops
