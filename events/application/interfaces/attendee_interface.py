from abc import abstractmethod
from typing import Protocol, List

from events.domain.models.attendee import AttendeeDM


class AttendeeCreator(Protocol):
    @abstractmethod
    async def create_attendee(self, attendee: AttendeeDM) -> None:
        ...
