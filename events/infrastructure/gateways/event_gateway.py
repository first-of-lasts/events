from typing import List
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from events.application.interfaces import event_interface
from events.infrastructure.persistence.models import Event


class EventGateway(
    event_interface.EventSaver
):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def save(self) -> None:
        pass
