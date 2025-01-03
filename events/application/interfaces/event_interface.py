from abc import abstractmethod
from typing import Protocol, List, Optional

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
    async def get_event(self, event_id: int) -> Optional[EventDM]:
        ...

    @abstractmethod
    async def get_detailed_event(
            self,
            event_id: int,
            language: str,
    ) -> Optional[event_response.EventDetail]:
        ...

    @abstractmethod
    async def get_user_events_list(
            self,
            language: str,
            user_id: int,
            limit: int,
            offset: int,
            sort_by: str,
            order: str,
    ) -> List[event_response.UserEventList]:
        ...

    @abstractmethod
    async def get_recommended_events_list(
            self,
            language: str,
            user_id: int,
            limit: int,
            offset: int,
            category_ids: Optional[List[int]],
            country_id: Optional[int],
            region_id: Optional[int],
    ) -> List[event_response.RecommendedEventList]:
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
