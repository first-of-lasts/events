from dataclasses import dataclass
from typing import Optional


@dataclass(slots=True)
class AttendeeDM:
    event_id: int
    user_id: int
