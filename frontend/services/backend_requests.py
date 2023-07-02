from datetime import date
from os import getenv

import requests
from loguru import logger


def recognize(image_bytes: bytes, task_id: str):
    files = {"upload_file": image_bytes}
    body = {"task_id": task_id}
    response = requests.post(
        f"{getenv('BACKEND_URI')}/recognize/", files=files, data=body
    )
    if response.status_code == 200:
        return response.json()
    return []


def get_analytics(start_date: date, end_date: date):
    return requests.get(
        f"{getenv('BACKEND_URI')}/analytics?date_start={start_date}&date_end={end_date}"
    ).json()


def get_all_students():
    return requests.get(f"{getenv('BACKEND_URI')}/student/").json()


def get_analytics_by_student_id(student_id, start_date, end_date):
    return requests.get(
        f"{getenv('BACKEND_URI')}/analytics/{student_id}?date_start={start_date}&date_end={end_date}",
    ).json()
