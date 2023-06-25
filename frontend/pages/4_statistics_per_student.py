from datetime import date, timedelta
from io import BytesIO
from os import getenv

import pandas as pd
import plotly.graph_objects as go
import requests
import streamlit as st


def _get_all_students():
    result = requests.get(f"{getenv('BACKEND_URI')}/students/").json()
    return result


def _get_student_statistics(student_id, start_date, end_date):
    result = requests.get(
        f"{getenv('BACKEND_URI')}/analytics/{student_id}?date_start={start_date}&date_end={end_date}"
    ).json()
    return result


st.set_page_config(page_title="Список студентов", page_icon="🧑")
with st.spinner("Загружаем список студентов..."):
    students_data = _get_all_students()
students_data = [res["track_id"] for res in students_data]


track_id = st.selectbox("Выберите студента", students_data)
start_date = st.date_input("Начало:", date.today() - timedelta(days=7))
end_date = st.date_input("Конец:", date.today())

is_pressed = st.button("Получить аналитику")

if is_pressed:
    with st.spinner("Считаем аналитику..."):
        result = _get_student_statistics(track_id, start_date, end_date)
        if result:
            df = pd.DataFrame(result)

            # Группировка данных по полю 'emotion'
            grouped_data = df.groupby("emotion")

            # Создание графиков для каждой эмоции
            fig = go.Figure()

            for emotion, data in grouped_data:
                fig.add_trace(
                    go.Scatter(
                        x=data["datetime"],
                        y=data["count"],
                        mode="lines+markers",
                        name=emotion,
                    )
                )

            # Вывод графика в Streamlit
            st.plotly_chart(fig)
        else:
            st.text("Нет данных за этот период")
