import datetime

from pydantic import BaseModel


class Call(BaseModel):
    source_phone: str
    target_phone_number: str
    duration_in_minutes: int
    start_time: datetime.date
