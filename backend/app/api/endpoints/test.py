import datetime

import streamlit as st
import pandas as pd
import numpy as np

chart_data = [
    {"datetime": datetime.date(2023, 6, 20), "emotion": "angry", "count": 37},
    {"datetime": datetime.date(2023, 6, 20), "emotion": "neutral", "count": 140},
    {"datetime": datetime.date(2023, 6, 20), "emotion": "fear", "count": 721},
    {"datetime": datetime.date(2023, 6, 20), "emotion": "sad", "count": 1200},
]

st.line_chart(chart_data)
