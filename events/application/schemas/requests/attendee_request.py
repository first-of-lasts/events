from pydantic import BaseModel


class AttendeeCreate(BaseModel):
    event_id: int
