from events.domain.models.event import EventDM
from events.application.interfaces import event_interface, user_interface
from events.application.dto import event as event_dto


class CreateEventInteractor:
    def __init__(
            self,
            event_gateway: event_interface.EventCreator,
            user_gateway: user_interface.UserReader
    ) -> None:
        self._event_gateway = event_gateway
        self._user_gateway = user_gateway

    async def __call__(self, dto: event_dto.NewEventDTO, email: str) -> None:
        user = await self._user_gateway.get_by_email(email)
        # TODO
        new_event = EventDM(

        )
        await self._event_gateway.create_event(new_event)
