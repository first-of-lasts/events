from abc import abstractmethod
from typing import Protocol

from events.domain.models.event import EventDM


class EventSaver(Protocol):
    @abstractmethod
    async def save(self, event: EventDM) -> None:
        pass
