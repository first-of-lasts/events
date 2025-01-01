from typing import List

from events.domain.models.event import EventDM
from events.application.interfaces import event_interface, user_interface
from events.application.services.location_validator import LocationValidator
from events.application.dto import event as event_dto


class CreateEventInteractor:
    def __init__(
            self,
            event_gateway: event_interface.EventCreator,
            user_gateway: user_interface.UserReader,
            location_validator: LocationValidator,
    ) -> None:
        self._event_gateway = event_gateway
        self._user_gateway = user_gateway
        self._location_validator = location_validator

    async def __call__(self, dto: event_dto.NewEventDTO, user_email: str) -> None:
        user = await self._user_gateway.get_by_email(user_email)
        await self._location_validator(dto.country_id, dto.region_id)
        new_event = EventDM(
            user_id=user.id,
            title=dto.title,
            description=dto.description,
            country_id=dto.country_id,
            region_id=dto.region_id,
        )
        await self._event_gateway.create_event(new_event)


class UpdateEventInteractor:
    def __init__(
            self,
            event_gateway: event_interface.EventUpdater,
            user_gateway: user_interface.UserReader,
            location_validator: LocationValidator,
    ) -> None:
        self._event_gateway = event_gateway
        self._user_gateway = user_gateway
        self._location_validator = location_validator

    async def __call__(self, dto: event_dto.UpdateEventDTO, user_email: str, event_id: int) -> None:
        user = await self._user_gateway.get_by_email(user_email)
        await self._location_validator(dto.country_id, dto.region_id)
        update_data = dto.model_dump()
        await self._event_gateway.update_event(
            user_id=user.id,event_id=event_id, update_data=update_data
        )


class ListUserEventsInteractor:
    def __init__(
            self,
            event_gateway: event_interface.EventReader,
            user_gateway: user_interface.UserReader,
    ) -> None:
        self._event_gateway = event_gateway
        self._user_gateway = user_gateway

    async def __call__(
            self,
            dto: event_dto.ListUserEventsDTO,
            user_email: str,
            language: str,
    ) -> List[EventDM]:
        user = await self._user_gateway.get_by_email(user_email)
        return await self._event_gateway.list_user_events(
            user_id=user.id,
            sort_by=dto.sort_by,
            order=dto.order,
            limit=dto.limit,
            offset=dto.offset,
            language=language,
        )
