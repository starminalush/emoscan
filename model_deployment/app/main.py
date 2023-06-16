import asyncio
import base64
import json

import cv2
import numpy as np
import ray
import torch
from facenet_pytorch import MTCNN
from fastapi import FastAPI
from loguru import logger
from models import EmotionRecognizer, FaceDetector, Tracker
from ray import serve
from schemas import Image

app = FastAPI()


def base64_to_numpy(image: str) -> np.ndarray:
    im_bytes = base64.b64decode(image)
    im_arr = np.frombuffer(im_bytes, dtype=np.uint8)  # im_arr is one-dim Numpy array
    return cv2.imdecode(im_arr, flags=cv2.IMREAD_COLOR)


@serve.deployment
@serve.ingress(app)
class FER:
    def __init__(
        self, face_detector_handler, emotion_recognition_handler, tracker_handler
    ):
        self.face_detector = face_detector_handler
        self.emotion_recognizer = emotion_recognition_handler
        self.tracker = tracker_handler

    @app.post("/")
    async def detect(self, image: Image):
        image = base64_to_numpy(image.img_bytes)
        result = await self.face_detector.remote(image)
        bboxes = await result

        emotion_recognitions_task = [
            self.emotion_recognizer.remote(image, bbox) for bbox in bboxes
        ]
        emotions = ray.get(await asyncio.gather(*emotion_recognitions_task))

        tracker_result = await self.tracker.remote(image, bboxes, emotions)
        return await tracker_result


backend = FER.bind(
    FaceDetector.bind(),
    EmotionRecognizer.bind(
        "s3://experiments/1/465e546c511f459196393bb26b978d3a/artifacts/onnx_model.onnx"
    ),
    Tracker.bind(),
)
