from datetime import date, timedelta
from os import getenv

import pandas as pd
import plotly.graph_objects as go
import requests
import streamlit as st


def _get_analytics(start_date: date, end_date: date):
    result = requests.get(f"{getenv('BACKEND_URI')}/analytics?date_start={start_date}&date_end={end_date}").json()
    return result


st.set_page_config(page_title="Аналитика эмоций по дням", page_icon="🕒")


start_date = st.date_input("Начало:", date.today() - timedelta(days=7))
end_date = st.date_input("Конец:", date.today())

is_pressed = st.button("Получить аналитику")
if is_pressed:
    with st.spinner("Считаем аналитику..."):
        result = _get_analytics(start_date, end_date)
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
