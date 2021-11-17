import abc
import typing as t

from ..protocols import FileReader


class Driver(abc.ABC):  # pragma: no cover
    @abc.abstractmethod
    async def write(self, path: str, data: t.IO[bytes]) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    async def read(self, path: str) -> FileReader:
        raise NotImplementedError

    @abc.abstractmethod
    async def exists(self, path: str) -> bool:
        raise NotImplementedError

    @abc.abstractmethod
    async def delete(self, path: str) -> None:
        raise NotImplementedError
