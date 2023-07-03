from datetime import date

from pydantic import BaseModel


class AnalyticsByRangeOfDates(BaseModel):
    emotion: str
    count: int
    date: date
