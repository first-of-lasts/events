from abc import abstractmethod
from contextlib import AbstractAsyncContextManager
from typing import Protocol


class DBSession(Protocol, ): # AbstractAsyncContextManager):
    @abstractmethod
    async def commit(self) -> None:
        ...

    @abstractmethod
    async def flush(self) -> None:
        ...

    @abstractmethod
    async def acquire_lock(self, table_name: str, lock_mode: str) -> None:
        ...

    @abstractmethod
    async def execute_query(
            self, query: str, params: dict | None = None
    ) -> None:
        ...
