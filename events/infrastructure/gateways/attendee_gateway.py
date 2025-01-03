from typing import List
from sqlalchemy import select, update, desc, asc, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from domain.exceptions.attendee import AttendeeAlreadyExistsError
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
        result = await self._session.execute(
            select(Attendee)
            .where(Attendee.event_id == attendee.event_id, Attendee.user_id == attendee.user_id)
        )
        existing_attendee = result.scalars().one_or_none()
        if existing_attendee:
            raise AttendeeAlreadyExistsError("Attendee already exists")
        new_attendee = Attendee(
            event_id=attendee.event_id,
            user_id=attendee.user_id
        )
        self._session.add(new_attendee)
        await self._session.commit()
