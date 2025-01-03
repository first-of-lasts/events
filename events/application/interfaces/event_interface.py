from abc import abstractmethod
from typing import Protocol, List

from events.domain.models.event import EventDM
from events.application.schemas.responses import event_response


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
    async def get_user_events_list(
            self,
            user_id: int,
            sort_by: str,
            order: str,
            limit: int,
            offset: int,
            language: str
    ) -> List[event_response.UserEventList]:
        ...


class EventDeleter(Protocol):
    @abstractmethod
    async def delete_event(self, event_id: int, user_id: int) -> None:
        ...


class CategoryReader(Protocol):
    @abstractmethod
    async def get_categories_list(
            self,
            language: str
    ) -> List[event_response.CategoryList]:
        ...
