import streamlit as st
from PIL import Image


def __load_image(image_file):
    img = Image.open(image_file)
    return img


st.set_page_config(page_title="Распознавание по изображению", page_icon="📷")
image_file = st.file_uploader("Загрузить фото", type=["png", "jpg", "jpeg"])

if image_file is not None:
    st.image(image_file, width=250)
    st.text("Загруженное фото")
    st.subheader("Результат распознавания")
    st.image(
        [__load_image("data/data2.png"), __load_image("data/data3.png")],
        width=250,
    )
    st.text(["Настроение: счастливое", "Настроение: нейтральное"])
