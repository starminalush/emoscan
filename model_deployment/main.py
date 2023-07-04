import asyncio
from os import getenv

from fastapi import FastAPI, UploadFile, File
import numpy as np
from ray import get, serve
from ray.serve.handle import RayServeHandle

from aliases import DetectionBbox
from converter import cnvt_bytes_to_numpy
from models import EmotionRecognizer, FaceDetector, Tracker
from schemas import RecognitionResult, TrackerResult

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

    @app.post("/predict/", response_model=list[RecognitionResult | None])
    async def recognize_emotions(
        self,
        upload_file: UploadFile = File(
            ..., content_type=["image/jpeg", "image/png", "image/jpg"]
        ),
    ):
        """Recognize emotions on all faces found in the photo.

        Args:
            upload_file: Input image.

        Returns:
            List containing the track_id label for each unique face, the bbox of the face, and the emotion class label.
        """
        image: np.ndarray = cnvt_bytes_to_numpy(upload_file.file.read())
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


backend = EmotionRecognitionPipeline.bind(
    FaceDetector.bind(),
    EmotionRecognizer.bind(getenv("MODEL_S3_PATH")),
    Tracker.bind(),
)
