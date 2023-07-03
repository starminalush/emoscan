from datetime import date
from os import getenv

import requests
from pydantic.tools import parse_obj_as

from data_classes import Analytics, EmotionRecognitionResult, Student


def recognize(
    image_bytes: bytes, task_id: str
) -> list[EmotionRecognitionResult | None]:
    """Get recognized emotions on image.

    Args:
        image_bytes: Input image or one of the video frames.
        task_id: TaskID. Ex: video ID of lesson id.

    Returns:
        List of dicts each containing face bbox, recognized emotion and track id.
    """
    files = {"upload_file": image_bytes}
    body = {"task_id": task_id}
    response = requests.post(
        f"{getenv('BACKEND_URI')}/recognize/", files=files, data=body
    )
    if response.status_code == 200:
        return [
            parse_obj_as(EmotionRecognitionResult, response_data)
            for response_data in response.json()
        ]
    return []


def get_analytics_by_range_of_dates(
    start_date: date, end_date: date
) -> list[Analytics | None]:
    """Get analytics by range of dates.

    Args:
        start_date: Range start date.
        end_date: Range end date.

    Returns:
        List of dicts each containing emotion, total number of emotions over range of dates and track_id.
    """
    response = requests.get(
        f"{getenv('BACKEND_URI')}/analytics?date_start={start_date}&date_end={end_date}"
    )
    if response.status_code == 200:
        return [
            parse_obj_as(Analytics, response_data) for response_data in response.json()
        ]
    return []


def get_all_students():
    """Get list of students' track ids.

    Returns:
        List containing all track_ids.
    """
    response = requests.get(f"{getenv('BACKEND_URI')}/student/")
    if response.status_code == 200:
        return [
            parse_obj_as(Student, response_data) for response_data in response.json()
        ]


def get_analytics_by_student_track_id(
    student_track_id, start_date, end_date
) -> list[Analytics | None]:
    """Get analytics by range of dates and student's track_id.

    Args:
        student_track_id:  Student's track ID.
        start_date: Range start date.
        end_date: Range end date.

    Returns:
        List of dicts each containing emotion, total number of emotions over range of dates and track_id.
    """
    response = requests.get(
        f"{getenv('BACKEND_URI')}/analytics/{student_track_id}?date_start={start_date}&date_end={end_date}"
    )
    if response.status_code == 200:
        return [
            parse_obj_as(Analytics, response_data) for response_data in response.json()
        ]
    return []
