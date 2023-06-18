import cv2
import mlflow
import numpy as np
import onnxruntime as nx
import torch
from deep_sort_realtime.deep_sort.track import Track
from deep_sort_realtime.deepsort_tracker import DeepSort
from mtcnn import MTCNN
from schemas import TrackerResult
from ray import serve
from aliases import InitialTrackerBbox, DetectionBbox


@serve.deployment(ray_actor_options={"num_cpus": 0, "num_gpus": 0.25})
class EmotionRecognizer:
    def __init__(self, model_uri):
        local_path = mlflow.artifacts.download_artifacts(model_uri)
        self.ort_session = nx.InferenceSession(
            local_path, providers=["CUDAExecutionProvider"]
        )
        self._idx_to_class: dict[int, str] = {
            0: "angry",
            1: "disgust",
            2: "fear",
            3: "happy",
            4: "neutral",
            5: "sad",
            6: "surprise",
        }

    def __call__(self, image: np.ndarray, bbox: DetectionBbox) -> str:
        bbox = [int(i) for i in bbox]
        face = image[bbox[1] : bbox[3], bbox[0] : bbox[2]]
        face = cv2.resize(face, (224, 224), interpolation = cv2.INTER_AREA)
        face = np.float32(face)
        face = face.transpose(2, 0, 1)
        face = face[np.newaxis, :]

        input_name = self.ort_session.get_inputs()[0].name
        ortvalue = nx.OrtValue.ortvalue_from_numpy(face, "cuda", 0)
        cls, _, _ = self.ort_session.run(None, {input_name: ortvalue})
        return self._idx_to_class[np.argmax(cls, 1)[0]]


@serve.deployment(ray_actor_options={"num_cpus": 0, "num_gpus": 0.25})
class FaceDetector:
    def __init__(self):
        self.model: MTCNN = MTCNN()

    def __call__(self, image: np.ndarray):
        boxes, _ = self.model.detect_faces(image)
        if len(boxes) > 0:
            return [item['box'] for item in boxes]
        else:
            return []

@serve.deployment(ray_actor_options={"num_cpus": 0, "num_gpus": 0.25})
class Tracker:
    def __init__(self):
        self.model: DeepSort = DeepSort(max_age=5, embedder="torchreid")

    def __call__(
        self, frame: np.ndarray, bboxes: list[DetectionBbox]
    ) -> list[TrackerResult]:
        tracker_bboxes: InitialTrackerBbox = [[bbox, 0, 0] for bbox in bboxes]
        tracks: list[Track] = self.model.update_tracks(
            raw_detections=tracker_bboxes, frame=frame
        )
        return [
            TrackerResult(track_id=track.track_id, bbox=track.to_ltwh().tolist())
            for track in tracks
        ]
