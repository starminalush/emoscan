from os import getenv

import streamlit as st
import requests

from utils import recognize


def __recognize(video_bytes) -> dict:
    files = {"file": video_bytes}
    response = requests.post(f"{getenv('BACKEND_URI')}/recognize/video", files=files)
    if response.status_code == 200:
        return response.json()
    return {}


st.set_page_config(page_title="Распознавание по изображению", page_icon="🎥")
video_file = st.file_uploader("Загрузить видеофайл", type=["mp4", "avi"])

if video_file is not None:
    c1, c2 = st.columns(2)
    c1.video(video_file)
    c1.text(video_file.name)
    with st.spinner("Распознаем..."):
        response = recognize(
            video_file.read(), uri=f"{getenv('BACKEND_URI')}/recognize/video"
        )
    if response:
        max_emotion = max(
            response["emotion_proportion"], key=response["emotion_proportion"].get
        )
        c2.markdown(
            f"""
        ПРЕВАЛИРУЮЩЕЕ НАСТРОЕНИЕ: {max_emotion}\n
    ДОЛИ ЭМОЦИЙ ПО ВРЕМЕНИ:\n
    \n
    {str(response["emotion_proportion"])}
        """
        )
        c2.button("Скачать видео с метками эмоций")
