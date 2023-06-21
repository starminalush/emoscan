from datetime import date

from pydantic import BaseModel


class AnalyticsPerRangeOfDates(BaseModel):
    emotion: str
    count: int
    datetime: date
