from abc import abstractmethod
from typing import Protocol

from events.domain.models.event import EventDM


class EventCreator(Protocol):
    @abstractmethod
    async def create_event(self, event: EventDM) -> None:
        ...
