from typing import List

from events.domain.exceptions.access import AuthenticationError
from events.domain.models.event import EventDM
from events.application.schemas.requests import event_request
from events.application.schemas.responses import event_response
from events.application.interfaces import event_interface
from events.application.interfaces import user_interface
from events.application.services.location_validator import LocationValidator


class CreateEventInteractor:
    def __init__(
            self,
            event_gateway: event_interface.EventCreator,
            location_validator: LocationValidator,
    ) -> None:
        self._event_gateway = event_gateway
        self._location_validator = location_validator

    async def __call__(self, dto: event_request.EventCreate, user_id: int) -> None:
        await self._location_validator(dto.country_id, dto.region_id)
        new_event = EventDM(
            user_id=user_id,
            title=dto.title,
            description=dto.description,
            starts_at=dto.starts_at,
            ends_at=dto.ends_at,
            category_ids=dto.category_ids,
            country_id=dto.country_id,
            region_id=dto.region_id,
        )
        await self._event_gateway.create_event(new_event)


class UpdateEventInteractor:
    def __init__(
            self,
            event_gateway: event_interface.EventUpdater,
            location_validator: LocationValidator,
    ) -> None:
        self._event_gateway = event_gateway
        self._location_validator = location_validator

    async def __call__(self, dto: event_request.EventUpdate, user_id: int, event_id: int) -> None:
        await self._location_validator(dto.country_id, dto.region_id)
        update_data = dto.model_dump()
        await self._event_gateway.update_event(
            user_id=user_id, event_id=event_id, update_data=update_data
        )


class ListUserEventsInteractor:
    def __init__(
            self,
            event_gateway: event_interface.EventReader,
    ) -> None:
        self._event_gateway = event_gateway

    async def __call__(
            self,
            dto: event_request.UserEventListFilter,
            user_id: int,
            language: str,
    ) -> List[event_response.UserEventList]:
        return await self._event_gateway.get_user_events_list(
            language=language,
            user_id=user_id,
            limit=dto.limit,
            offset=dto.offset,
            sort_by=dto.sort_by,
            order=dto.order,
        )


class DeleteEventInteractor:
    def __init__(
            self,
            event_gateway: event_interface.EventDeleter,
    ):
        self._event_gateway = event_gateway

    async def __call__(self, event_id: int, user_id: int) -> None:
        await self._event_gateway.delete_event(
            event_id=event_id, user_id=user_id
        )


class ListCategoriesInteractor:
    def __init__(
            self,
            event_gateway: event_interface.CategoryReader,
    ):
        self._event_gateway = event_gateway

    async def __call__(
            self,
            language: str
    ) -> List[event_response.CategoryList]:
        categories = await self._event_gateway.get_categories_list(language)
        return categories


class ListRecommendedEventsInteractor:
    def __init__(
            self,
            event_gateway: event_interface.EventReader,
            user_gateway: user_interface.UserReader,
    ):
        self._event_gateway = event_gateway
        self._user_gateway = user_gateway

    async def __call__(
            self,
            dto: event_request.RecommendedEventListFilter,
            user_id: int,
            language: str,
    ) -> List[event_response.RecommendedEventList]:
        if not dto.country_id:
            user = await self._user_gateway.get_user_by_id(user_id)
            if not user:
                raise AuthenticationError("User not found")
            dto.country_id = user.country_id
        return await self._event_gateway.get_recommended_events_list(
            language=language,
            user_id=user_id,
            limit=dto.limit,
            offset=dto.offset,
            category_ids=dto.category_ids,
            country_id=dto.country_id,
            region_id=dto.region_id,
        )
