import typing
from abc import ABC, abstractmethod
from types import TracebackType


class AbstractUnitOfWork(ABC):
    session: typing.Any = None

    @classmethod
    async def dependency(cls) -> typing.Generator:
        async with cls() as uow:
            yield uow

    @abstractmethod
    def __init__(self) -> None:
        pass

    @abstractmethod
    async def __aenter__(self) -> 'AbstractUnitOfWork':
        pass

    @abstractmethod
    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        tb: TracebackType | None,
    ) -> None:
        pass

    @abstractmethod
    def add(self, entity: typing.Any) -> None:
        pass

    @abstractmethod
    async def flush(self) -> None:
        pass

    @abstractmethod
    async def refresh(
        self, entity: typing.Any, attribute_names: typing.Iterable[str] | None = None
    ) -> None:
        pass

    @abstractmethod
    async def delete(self, entity: typing.Any) -> None:
        pass
