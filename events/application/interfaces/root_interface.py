from abc import abstractmethod
from typing import Protocol


class DBSession(Protocol):
    @abstractmethod
    async def commit(self) -> None:
        ...

    @abstractmethod
    async def flush(self) -> None:
        ...

    @abstractmethod
    def begin(self) -> None:
        ...

    @abstractmethod
    async def execute_query(
            self, query: str, params: dict | None = None
    ) -> None:
        ...
