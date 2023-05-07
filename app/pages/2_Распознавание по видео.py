import streamlit as st
from PIL import Image


def __load_image(image_file):
    img = Image.open(image_file)
    return img


st.set_page_config(page_title="Распознавание по изображению", page_icon="🎥")
video_file = st.file_uploader("Загрузить видеофайл", type=["mp4", "avi"])

if video_file is not None:
    for i in range(1):
        c1, c2 = st.columns(2)
        c1.image(__load_image("data/data4.jpg"), width=250)
        c1.text("Rick Astley — Never Gonna Give You Up")
        c2.markdown(
            """
        ПРЕВАЛИРУЮЩЕЕ НАСТРОЕНИЕ: СЧАСТЛИВОЕ\n
    ДОЛИ ЭМОЦИЙ ПО ВРЕМЕНИ:\n
    \n
     - 52% - счастливое\n
     - 42% - нейтральное\n
     - 6% - негативное\n
        """
        )
        c2.button("Скачать видео с метками эмоций")
