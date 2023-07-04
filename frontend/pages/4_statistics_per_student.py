from datetime import date, timedelta

import streamlit as st

from services.backend_requests import (
    get_all_students,
    get_analytics_by_student_track_id,
)
from services.plots import plot_analytics

st.set_page_config(page_title="Список студентов", page_icon="🧑")

with st.spinner("Загружаем список студентов..."):
    students_data = get_all_students()
students_data = [student.track_id for student in students_data]


track_id = st.selectbox("Выберите студента", students_data)
start_date = st.date_input("Начало:", date.today() - timedelta(days=7))
end_date = st.date_input("Конец:", date.today())

is_pressed = st.button("Получить аналитику")

if is_pressed:
    with st.spinner("Считаем аналитику..."):
        analytics = get_analytics_by_student_track_id(track_id, start_date, end_date)
        if analytics:
            fig = plot_analytics(analytics)
            st.plotly_chart(fig)
        else:
            st.text("Нет данных за этот период")
