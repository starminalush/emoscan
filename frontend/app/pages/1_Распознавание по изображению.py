import base64
from io import BytesIO
from loguru import logger
import streamlit as st
from PIL import Image
import requests


def __crop_face( bbox, image_file):
    image = Image.open(image_file)
    logger.error(bbox)
    return image.crop(bbox)


def __recognize(image_bytes):
    files = {"file": image_bytes}
    response = requests.post("http://backend:8000/recognize/", files=files)
    if response.status_code == 200:
        return response.json()
    return None


st.set_page_config(page_title="Распознавание по изображению", page_icon="📷")
image_file = st.file_uploader("Загрузить фото", type=["png", "jpg", "jpeg"])

if image_file is not None:

    st.image(image_file, width=250)
    st.text("Загруженное фото")
    st.subheader("Результат распознавания")
    with st.spinner('Wait for it...'):
        recognized_data = __recognize(image_bytes=image_file.read())
    if recognized_data:
        #получили боксы
        for res in recognized_data:
            st.image(
                __crop_face(res["bbox"], image_file),
                width=250,
            )
            st.text(res["emotion"])
    else:
        st.text("Не удалось распознать лицо или эмоции. Пожалуйста, проверьте файл")
