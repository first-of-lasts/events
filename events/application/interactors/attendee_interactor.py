from typing import List

from events.domain.models.attendee import AttendeeDM
from events.application.interfaces import attendee_interface
from events.application.schemas.requests import attendee_request
from events.application.schemas.responses import attendee_response



class CreateAttendeeInteractor:
    def __init__(
            self,
            attendee_gateway: attendee_interface.AttendeeCreator,
    ) -> None:
        self._attendee_gateway = attendee_gateway

    async def __call__(self, dto: attendee_request.AttendeeCreate, user_id: int) -> None:
        new_attendee = AttendeeDM(
            event_id=dto.event_id,
            user_id=user_id,
        )
        await self._attendee_gateway.create_attendee(new_attendee)
