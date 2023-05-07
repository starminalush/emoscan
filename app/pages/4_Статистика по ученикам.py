import numpy as np
import streamlit as st
from matplotlib import pyplot as plt
from PIL import Image


def __plot_bar_chart():
    plt.rcdefaults()
    fig, ax = plt.subplots()

    # Example data
    people = ("Негативное", "Позитивное", "Нейтральное")
    y_pos = np.arange(len(people))
    performance = 10 * np.random.rand(3)

    ax.barh(y_pos, performance, align="center")
    ax.set_yticks(y_pos, labels=people)
    ax.invert_yaxis()  # labels read top-to-bottom
    ax.set_xlabel("Количество занятий")

    return fig


def __load_image(image_file):
    img = Image.open(image_file)
    return img


for i in range(2, 4):
    c1, mid, c2 = st.columns([2, 1, 3])
    c1.image(
        __load_image(f"data/data{i}.png"),
        width=250,
    )
    c2.write(__plot_bar_chart())
