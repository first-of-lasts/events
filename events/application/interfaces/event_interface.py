from abc import abstractmethod
from typing import Protocol, List

from events.domain.models.event import EventDM


class EventCreator(Protocol):
    @abstractmethod
    async def create_event(self, event: EventDM) -> None:
        ...


class EventUpdater(Protocol):
    @abstractmethod
    async def update_event(self, user_id: int, event_id: int, update_data: dict) -> None:
        ...


class EventReader(Protocol):
    @abstractmethod
    async def list_user_events(
            self,
            user_id: int,
            sort_by: str,
            order: str,
            limit: int,
            offset: int,
            language: str
    ) -> List[EventDM]:
        ...
