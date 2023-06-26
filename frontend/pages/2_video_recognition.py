from os import getenv

import requests
import streamlit as st

from utils import recognize


def __recognize(video_bytes) -> dict:
    files = {"file": video_bytes}
    response = requests.post(f"{getenv('BACKEND_URI')}/recognize/video", files=files)
    if response.status_code == 200:
        return response.json()
    return {}


st.set_page_config(page_title="Распознавание по видео", page_icon="🎥")
video_file = st.file_uploader("Загрузить видеофайл", type=["mp4", "avi"])

if video_file is not None:
    c1, c2 = st.columns(2)
    c1.video(video_file, start_time=5)
    c1.text(video_file.name)
    with st.spinner("Распознаем..."):
        response = recognize(video_file.read(), uri=f"{getenv('BACKEND_URI')}/recognize/video")
    if response:
        max_emotion = max(response["emotion_proportion"], key=response["emotion_proportion"].get)
        result = "\n".join(f"{key}: {value:.2f}%" for key, value in response["emotion_proportion"].items())
        c2.write(
            f"""
            ПРЕВАЛИРУЮЩЕЕ НАСТРОЕНИЕ: {max_emotion}\n
            ДОЛИ ЭМОЦИЙ ПО ВРЕМЕНИ:\n
            \n
            {result}
            """
        )
        c2.button("Скачать видео с метками эмоций")
