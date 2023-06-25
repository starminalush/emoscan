from io import BytesIO
from os import getenv

import streamlit as st
import requests
from PIL  import Image
from st_clickable_images import clickable_images
from loguru import logger

def _get_all_students(page, limit):
    result = requests.get(f"{getenv('BACKEND_URI')}/students/?page={page}&limit={limit}").json()
    return result


def _crop_face(image_url, bbox):
    image = Image.open(BytesIO(requests.get(url=image_url).content))
    return image.crop(bbox)

st.set_page_config(page_title="Список студентов", page_icon="🧑")
page = st.sidebar.number_input("Страница", value=1, min_value=1)
with st.spinner("Загружаем список студентов..."):
    students_data = _get_all_students(page=page, limit=10)
    for data in students_data:
        st.image(_crop_face(data['image_url'], data["bbox"]), width=250)
        st.markdown(data['track_id'])


