import cv2
import mlflow
import numpy as np
import onnxruntime as nx
import torch
from deep_sort_realtime.deep_sort.track import Track
from deep_sort_realtime.deepsort_tracker import DeepSort
from facenet_pytorch.models.mtcnn import MTCNN
from ray import serve

from aliases import DetectionBbox, InitialTrackerBbox
from schemas import TrackerResult
from utils import postprocess_bbox


@serve.deployment(ray_actor_options={"num_cpus": 0, "num_gpus": 0.25})
class EmotionRecognizer:
    def __init__(self, model_uri):
        local_path: str = mlflow.artifacts.download_artifacts(model_uri)
        self.ort_session = nx.InferenceSession(
            local_path, providers=["CUDAExecutionProvider"]
        )
        self._idx_to_class: dict[int, str] = {
            0: "angry",
            1: "disgust",
            2: "happy",
            3: "fear",
            4: "sad",
            5: "neutral",
            6: "surprise",
        }

    def __call__(self, image: np.ndarray, bbox: DetectionBbox) -> str:
        """Classify facial expressions.

        Args:
            image: Input image(full).
            bbox: Face bbox.

        Returns:
            Facial expression label.
        """
        bbox = [int(coord) for coord in bbox]
        face = image[bbox[1] : bbox[3], bbox[0] : bbox[2]]
        face = cv2.resize(face, (224, 224))
        face = np.float32(face)
        face = face.transpose(2, 0, 1)
        face = face[np.newaxis, :]

        input_name = self.ort_session.get_inputs()[0].name
        ortvalue = nx.OrtValue.ortvalue_from_numpy(face, "cuda", 0)
        label, _, _ = self.ort_session.run(None, {input_name: ortvalue})
        return self._idx_to_class[np.argmax(label, 1)[0]]


@serve.deployment(ray_actor_options={"num_cpus": 0, "num_gpus": 0.25})
class FaceDetector:
    def __init__(self):
        self.model: MTCNN = MTCNN(image_size=640, device=torch.device("cuda:0"))

    def __call__(self, image: np.ndarray):
        """Detect faces on image.

        Args:
            image: Input image(full).

        Returns:
            List of faces' bboxes.
        """
        bboxes, _ = self.model.detect(image)
        if isinstance(bboxes, np.ndarray):
            return [
                postprocessed_bbox
                for bbox in bboxes
                if (postprocessed_bbox := postprocess_bbox(bbox.tolist())) is not None
            ]
        return []


@serve.deployment(ray_actor_options={"num_cpus": 0, "num_gpus": 0.25})
class Tracker:
    def __init__(self):
        self.model: DeepSort = DeepSort(max_age=5, embedder="torchreid")

    def __call__(
        self, frame: np.ndarray, bboxes: list[DetectionBbox]
    ) -> list[TrackerResult]:
        """Track face by face's bbox.

        Args:
            frame: Input image(full).
            bboxes: Bboxes of found faces.

        Returns:
            TrackID of face.
        """
        tracker_bboxes: InitialTrackerBbox = [[bbox, 0, 0] for bbox in bboxes]
        tracks: list[Track] = self.model.update_tracks(
            raw_detections=tracker_bboxes, frame=frame
        )
        postprocessed_tracks = [
            track
            for track in tracks
            if postprocess_bbox(track.to_ltwh().tolist())
        ]
        return [
            TrackerResult(
                track_id=track.track_id,
                bbox=[0 if coord < 0 else coord for coord in track.to_ltwh().tolist()],
            )
            for track in postprocessed_tracks
        ]
