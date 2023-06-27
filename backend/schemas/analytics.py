from datetime import date

from pydantic import BaseModel


class AnalyticsByRangeOfDates(BaseModel):
    emotion: str
    count: int
    datetime: date


class AnalyticsByStudentID(BaseModel):
    emotion: str
    count: int
    datetime: date
