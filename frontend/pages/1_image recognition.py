from uuid import uuid4

import streamlit as st
from utils import recognize, crop_face

st.set_page_config(page_title="Распознавание по изображению", page_icon="📷")
image_file = st.file_uploader("Загрузить фото", type=["png", "jpg", "jpeg"])

if image_file is not None:
    st.image(image_file, width=250)
    st.text("Загруженное фото")
    with st.spinner("Распознаем..."):
        task_id = str(uuid4())
        recognized_data = recognize(image_bytes=image_file.read(), task_id=task_id)
    st.subheader("Результат распознавания")
    grid = st.columns(5)
    col = 0
    if recognized_data:
        for data in recognized_data:
            with grid[col]:
                st.image(
                    crop_face(bbox=data["bbox"], image_file=image_file),
                    width=100,
                    caption=f"Настроение: {data['emotion']}",
                )
            col = (col + 1) % 5
    else:
        st.text("Не удалось распознать лицо или эмоции. Пожалуйста, проверьте файл")
