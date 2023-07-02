import itertools
import tempfile
import uuid
from collections import Counter
from pathlib import Path

import streamlit as st
from converters import cnvt_image_to_bytes
from services.backend_requests import recognize
from services.video_frame_extractor import extract_frames_from_video

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
    preview_image = next(itertools.islice(frames_generator, 10, None))
    c1.image(preview_image, width=250)
    c1.text(video_file.name)
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
        counter = Counter()
        counter.update([res["emotion"] for res in recognition_results])

        if counter.total() > 0:
            emotion_percentages = {
                emotion: count / counter.total() * 100
                for emotion, count in counter.items()
            }
            emotions_percentages = {
                k: v
                for k, v in sorted(
                    emotion_percentages.items(), key=lambda item: item[1], reverse=True
                )
            }
            max_emotion = list(emotions_percentages.keys())[0]
            c2.write(f"ПРЕВАЛИРУЮЩЕЕ НАСТРОЕНИЕ: {max_emotion}\n")
            c2.write("ДОЛИ ЭМОЦИЙ ПО ВРЕМЕНИ: \n")
            for emotion, proportion in emotions_percentages.items():
                c2.text(f"{emotion}: {proportion:.2f}%")

            c2.button("Скачать видео с метками эмоций")
        else:
            c2.write(
                "Не удалось распознать эмоции. Возможно, на загруженном видео нет людей."
            )
