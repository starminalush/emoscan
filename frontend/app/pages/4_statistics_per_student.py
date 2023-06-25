from os import getenv

import streamlit as st
import requests
from operator import itemgetter
import itertools


def _get_all_students():
    result = requests.get(f"{getenv('BACKEND_URI')}/students/").json()
    return result


st.set_page_config(page_title="Список студентов", page_icon="🧑")
with st.spinner("Загружаем список студентов..."):
    students_data = _get_all_students()
#
#
# logger.info(students_data)
images = [item["image_url"] for item in students_data]
titles = [item["track_id"] for item in students_data]


def paginator(label, items, items_per_page=10, on_sidebar=True):
    # Figure out where to display the paginator
    if on_sidebar:
        location = st.sidebar.empty()
    else:
        location = st.empty()

    # Display a pagination selectbox in the specified location.
    items = list(items)
    n_pages = len(items)
    n_pages = (len(items) - 1) // items_per_page + 1
    page_format_func = lambda i: "Page %s" % i
    page_number = location.selectbox(
        label, range(n_pages), format_func=page_format_func
    )

    # Iterate over the items in the page to let the user display them.
    min_index = page_number * items_per_page
    max_index = min_index + items_per_page
    return itertools.islice(enumerate(items), min_index, max_index)


def demonstrate_image_pagination():
    image_iterator = paginator("Select a student page", images)
    indices_on_page, images_on_page = map(list, zip(*image_iterator))
    st.image(
        images_on_page,
        width=100,
        caption=titles[indices_on_page[0] : indices_on_page[:-1]],
    )
