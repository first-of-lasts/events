from dataclasses import dataclass
from typing import Optional


@dataclass(slots=True)
class AttendeeDM:
    id: Optional[int] = None
