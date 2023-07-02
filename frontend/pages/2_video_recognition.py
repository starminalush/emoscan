import itertools
import tempfile
import uuid
from os import getenv
from pathlib import Path
from collections import Counter

import requests
import streamlit as st

from converters import cnvt_image_to_bytes
from utils import recognize
from services.video_frame_extractor import extract_frames_from_video


def __recognize(video_bytes) -> dict:
    files = {"file": video_bytes}
    response = requests.post(f"{getenv('BACKEND_URI')}/recognize/video", files=files)
    if response.status_code == 200:
        return response.json()
    return {}


st.set_page_config(page_title="Распознавание по видео", page_icon="🎥")
video_file = st.file_uploader("Загрузить видеофайл", type=["mp4", "avi"])

if video_file is not None:
    with tempfile.NamedTemporaryFile(
            suffix=Path(video_file.name).suffix, delete=False
    ) as temp_video_file:
        temp_video_file.write(video_file.read())
    task_id = str(uuid.uuid4())
    # берем каждый 5 кадр
    frames_generator = extract_frames_from_video(temp_video_file.name, frame_count=5)
    c1, c2 = st.columns(2)
    preview_image = next(itertools.islice(frames_generator, 10,  None))
    c1.image(preview_image, width=250)
    c1.text(video_file.name)
    with st.spinner("Распознаем..."):
        recognition_results = [recognize(image_bytes=cnvt_image_to_bytes(frame), task_id=task_id) for frame in frames_generator]
        recognition_results = [
            recognition_result
            for sublist in recognition_results
            for recognition_result in sublist
        ]
    if recognition_results:
        counter = Counter()
        counter.update([res['emotion'] for res in recognition_results])

        if counter.total() > 0:
            emotion_percentages = {
                emotion: count / counter.total() * 100 for emotion, count in counter.items()
            }
        emotion_percentages = {k: v for k, v in sorted(emotion_percentages.items(), key=lambda item: item[1], reverse=True)}
        max_emotion =  list(emotion_percentages.keys())[0]
        c2.write(
            f"ПРЕВАЛИРУЮЩЕЕ НАСТРОЕНИЕ: {max_emotion}\n")
        c2.write("ДОЛИ ЭМОЦИЙ ПО ВРЕМЕНИ: \n")
        for key, value in emotion_percentages.items():
            c2.text(f"{key}: {value:.2f}%")

        c2.button("Скачать видео с метками эмоций")
