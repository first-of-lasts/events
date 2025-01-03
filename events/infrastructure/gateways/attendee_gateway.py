from typing import List
from sqlalchemy import select, update, desc, asc, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from events.domain.models.attendee import AttendeeDM
from events.application.interfaces import attendee_interface
from events.application.schemas.responses import attendee_response
from events.infrastructure.persistence.models import Attendee


class AttendeeGateway(
    attendee_interface.AttendeeCreator,
):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def create_attendee(self, attendee: AttendeeDM) -> None:
        new_attendee = Attendee(

        )
        self._session.add(new_attendee)
        await self._session.commit()
