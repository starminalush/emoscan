import itertools
from pathlib import Path
import tempfile
import uuid

import streamlit as st

from converters import cnvt_image_to_bytes
from services.backend_requests import recognize
from services.plots import plot_emotion_percentage
from services.statistics import get_statictics_of_emotion
from services.video_frame_extractor import extract_frames_from_video

st.set_page_config(page_title="Распознавание по видео", page_icon="🎥")

video_file = st.file_uploader("Загрузить видеофайл", type=["mp4", "avi"])

if video_file is not None:
    with tempfile.NamedTemporaryFile(
        suffix=Path(video_file.name).suffix, delete=False
    ) as temp_video_file:
        temp_video_file.write(video_file.read())
        temp_video_file_name = temp_video_file.name

    frames_generator = extract_frames_from_video(temp_video_file_name, frame_count=5)

    c1, c2 = st.columns(2)
    preview_image = next(itertools.islice(frames_generator, 10, None))
    c1.image(preview_image, width=250)

    task_id = str(uuid.uuid4())
    with st.spinner("Распознаем..."):
        recognition_results = [
            recognize(image_bytes=cnvt_image_to_bytes(frame), task_id=task_id)
            for frame in frames_generator
        ]
        recognition_results = [
            recognition_result
            for sublist in recognition_results
            for recognition_result in sublist
        ]
    if recognition_results:
        emotion_proportions = get_statictics_of_emotion(
            emotions=[
                recognition_result.emotion for recognition_result in recognition_results
            ]
        )
        fig = plot_emotion_percentage(emotion_proportions)
        st.subheader("Аналитика эмоций на видео")
        st.plotly_chart(fig, use_container_width=True)

        c2.button("Скачать видео с метками эмоций")
    else:
        c2.write(
            "Не удалось распознать эмоции. Возможно, на загруженном видео нет людей."
        )
