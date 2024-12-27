from abc import abstractmethod
from typing import Protocol


class EventSaver(Protocol):
    @abstractmethod
    async def save(self) -> None:
        pass
