from events.application.interfaces import event_interface
from events.application.dto.event import NewEventDTO


class CreateEventInteractor:
    def __init__(
            self,
            event_gateway: event_interface.EventSaver,
    ) -> None:
        self._event_gateway = event_gateway

    async def __call__(self, event_dto: NewEventDTO, email: str) -> None:
        print("EVENT DTO", event_dto)

        # TODO get user from email
        return await self._event_gateway.save()
