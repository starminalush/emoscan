from copy import copy

import cv2
import mlflow
import numpy as np
import onnxruntime as nx
import torch
from deep_sort_realtime.deepsort_tracker import DeepSort
from facenet_pytorch import MTCNN
from ray import serve


@serve.deployment
class EmotionRecognizer:
    def __init__(self, model_uri):
        local_path = mlflow.artifacts.download_artifacts(model_uri)
        self.ort_session = nx.InferenceSession(
            local_path, providers=["CPUExecutionProvider"]
        )

    def __call__(self, image, bbox) -> str:
        bbox = [int(i) for i in bbox]
        face = image[bbox[1] : bbox[3], bbox[0] : bbox[2]]
        face = cv2.resize(face, (224, 224))
        face = np.float32(face)
        face = face.transpose(2, 0, 1)
        face = face[np.newaxis, :]

        input_name = self.ort_session.get_inputs()[0].name
        ortvalue = nx.OrtValue.ortvalue_from_numpy(face, "cpu", 0)
        cls, _, _ = self.ort_session.run(None, {input_name: ortvalue})
        return str(np.argmax(cls, 1)[0])


@serve.deployment
class FaceDetector:
    def __init__(self):
        device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
        self.model = MTCNN(image_size=640, device=device)

    def __call__(self, image: np.ndarray):
        boxes, _ = self.model.detect(image)
        return boxes.tolist()


@serve.deployment
class Tracker:
    def __init__(self):
        self.model = DeepSort(max_age=5)

    def __call__(self, frame, bboxes, emotions):
        detections = []
        detected_result = []
        for emotion, bbox in zip(emotions, bboxes):
            detections.append((bbox, 0, emotion))
        tracks = self.model.update_tracks(detected_result, frame=frame)
        for track in tracks:
            if not track.is_confirmed():
                continue
            track_id = track.track_id
            ltrb = track.to_ltrb()
            class_emotion = track.det_class

            detections.append(
                {"bbox": ltrb, "tracking_id": track_id, "class_emotion": class_emotion}
            )
        return detections
