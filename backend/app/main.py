import cv2
import numpy as np
from ray import serve
import onnxruntime as nx
from dotenv import load_dotenv
import mlflow
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import PlainTextResponse

load_dotenv()

app = FastAPI()


@serve.deployment(
    num_replicas=1, ray_actor_options={"num_cpus": 0.2, "num_gpus": 0}, route_prefix="/"
)
@serve.ingress(app)
class FERDeployment:
    def __init__(self, model_uri):
        local_path = mlflow.artifacts.download_artifacts(model_uri)
        self.ort_session = nx.InferenceSession(local_path)

    def load_image_into_numpy_array(self, data):
        return cv2.imdecode(np.frombuffer(data, np.uint8), -1)

    @app.post("/dan", response_class=PlainTextResponse)
    async def classify(self, image: UploadFile = File(...)):
        image_np = self.load_image_into_numpy_array(await image.read())
        image_np = cv2.resize(image_np, (224, 224))
        image_np = np.float32(image_np)
        img = image_np.transpose(2, 0, 1)
        img = np.expand_dims(img, axis=0)

        input_name = self.ort_session.get_inputs()[0].name
        print(input_name)
        ortvalue = nx.OrtValue.ortvalue_from_numpy(img, "cpu", 0)
        cls, feature, heads = self.ort_session.run(None, {input_name: ortvalue})
        return str(np.argmax(cls, 1)[0])


backend = FERDeployment.bind(
    "s3://experiments/1/465e546c511f459196393bb26b978d3a/artifacts/onnx_model.onnx"
)
