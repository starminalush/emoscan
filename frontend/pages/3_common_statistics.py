from datetime import date, timedelta

import streamlit as st

from services.backend_requests import get_analytics_by_range_of_dates
from services.plots import plot_analytics

st.set_page_config(page_title="Аналитика эмоций по дням", page_icon="🕒")

start_date = st.date_input("Начало:", date.today() - timedelta(days=7))
end_date = st.date_input("Конец:", date.today())

is_pressed = st.button("Получить аналитику")
if is_pressed:
    with st.spinner("Считаем аналитику..."):
        analytics = get_analytics_by_range_of_dates(start_date, end_date)
        if analytics:
            fig = plot_analytics(analytics)
            st.plotly_chart(fig)
        else:
            st.text("Нет данных за этот период")
