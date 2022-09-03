import datetime

from pydantic import BaseModel


class CallSchema(BaseModel):
    source_phone: str
    target_phone_number: str
    duration_in_minutes: int
    start_time: datetime.datetime
