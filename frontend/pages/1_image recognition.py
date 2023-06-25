from os import getenv

import requests
import streamlit as st
from PIL import Image


def __crop_face(bbox: list[int], image_file: bytes) -> Image:
    image = Image.open(image_file)
    return image.crop(bbox)


def __recognize(image_bytes) -> list[dict[str, str | list[int]] | dict]:
    files = {"file": image_bytes}
    response = requests.post(f"{getenv('BACKEND_URI')}/recognize/image", files=files)
    if response.status_code == 200:
        return response.json()
    return []


st.set_page_config(page_title="Распознавание по изображению", page_icon="📷")
image_file = st.file_uploader("Загрузить фото", type=["png", "jpg", "jpeg"])

if image_file is not None:
    st.image(image_file, width=250)
    st.text("Загруженное фото")
    with st.spinner("Распознаем..."):
        recognized_data = __recognize(image_bytes=image_file.read())
    st.subheader("Результат распознавания")
    grid = st.columns(5)
    col = 0
    if recognized_data:
        for data in recognized_data:
            with grid[col]:
                st.image(
                    __crop_face(data["bbox"], image_file),
                    width=100,
                    caption=f"Настроение: {data['emotion']}",
                )
            col = (col + 1) % 5
    else:
        st.text("Не удалось распознать лицо или эмоции. Пожалуйста, проверьте файл")
