import asyncio
from os import getenv

import numpy as np
from fastapi import FastAPI
from ray import get, serve
from ray.serve.handle import RayServeHandle

from aliases import DetectionBbox
from converter import cnvt_base64_to_numpy
from models import EmotionRecognizer, FaceDetector, Tracker
from schemas import Image, RecognitionResult, TrackerResult

app = FastAPI()


@serve.deployment
@serve.ingress(app)
class EmotionRecognitionPipeline:
    def __init__(
        self,
        face_detector_handler: RayServeHandle,
        emotion_recognition_handler: RayServeHandle,
        tracker_handler: RayServeHandle,
    ):
        self.face_detector = face_detector_handler
        self.emotion_recognizer = emotion_recognition_handler
        self.tracker = tracker_handler

    @app.post("/", response_model=list[RecognitionResult | None])
    async def recognize_emotions(self, image: Image):
        """Recognize emotions on all faces found in the photo.

        Args:
            image: Input image.

        Returns:
            List containing the track_id label for each unique face, the bbox of the face, and the emotion class label.
        """
        image: np.ndarray = cnvt_base64_to_numpy(image.base64_image)
        bboxes: list[DetectionBbox | None] = await (
            await self.face_detector.remote(image)
        )
        if bboxes:
            tracker_results: list[TrackerResult] = get(
                await self.tracker.remote(image, bboxes)
            )
            emotion_recognition_tasks = [
                self.emotion_recognizer.remote(
                    image, list(map(int, tracker_result.bbox))
                )
                for tracker_result in tracker_results
            ]
            emotions = get(await asyncio.gather(*emotion_recognition_tasks))
            return [
                RecognitionResult(
                    emotion=emotion,
                    track_id=tracker_result.track_id,
                    bbox=tracker_result.bbox,
                )
                for emotion, tracker_result in zip(emotions, tracker_results)
            ]
        return []


app = EmotionRecognitionPipeline.bind(
    FaceDetector.bind(),
    EmotionRecognizer.bind(getenv("MODEL_S3_PATH")),
    Tracker.bind(),
)
