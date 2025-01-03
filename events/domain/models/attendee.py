from dataclasses import dataclass


@dataclass(slots=True)
class AttendeeDM:
    event_id: int
    user_id: int
