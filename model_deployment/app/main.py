import asyncio

import numpy as np
import ray
from fastapi import FastAPI
from models import EmotionRecognizer, FaceDetector, Tracker
from ray import serve
from schemas import Image, RecognitionResult, TrackerResult
from utils import base64_to_numpy


app = FastAPI()


@serve.deployment
@serve.ingress(app)
class FER:
    def __init__(
        self, face_detector_handler, emotion_recognition_handler, tracker_handler
    ):
        self.face_detector = face_detector_handler
        self.emotion_recognizer = emotion_recognition_handler
        self.tracker = tracker_handler

    @app.post("/", response_model=list[RecognitionResult])
    async def detect(self, image: Image):
        image: np.ndarray = base64_to_numpy(image.img_bytes)
        bboxes = await (await self.face_detector.remote(image))

        tracker_results: list[TrackerResult] = ray.get(
            await self.tracker.remote(image, bboxes)
        )
        for t in tracker_results:
            ray.logger.info(t)
            ray.logger.info(t.track_id)

        emotion_recognition_tasks = [
            self.emotion_recognizer.remote(image, tracker_result.bbox)
            for tracker_result in tracker_results
        ]
        emotions = ray.get(await asyncio.gather(*emotion_recognition_tasks))
        return [
            {"emotion": emotion, "track_id": item.track_id, "bbox": item.bbox}
            for emotion, item in zip(emotions, tracker_results)
        ]


backend = FER.bind(
    FaceDetector.bind(),
    EmotionRecognizer.bind(
        "s3://experiments/1/465e546c511f459196393bb26b978d3a/artifacts/onnx_model.onnx"
    ),
    Tracker.bind(),
)
