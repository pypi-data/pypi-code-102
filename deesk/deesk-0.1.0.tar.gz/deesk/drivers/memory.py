from __future__ import annotations

import io
import typing as t
from os import PathLike

from deesk.drivers.base import Driver
from deesk.protocols import FileReader


class TmpFile:
    def __init__(self, max_size: int = 1) -> None:
        self._io = io.BytesIO()
        self._bytes_written = 0
        self._max_size = max_size

    async def write(self, data: bytes) -> None:
        self._bytes_written += len(data)
        self._io.write(data)

    async def read(self, size: int = -1) -> bytes:
        return self._io.read(size)

    async def seek(self, position: int) -> None:
        self._io.seek(position)

    async def __aenter__(self) -> TmpFile:
        return self

    async def __aexit__(self, *args: t.Any) -> None:
        pass


class MemoryDriver(Driver):
    def __init__(self, max_size: int = 1024 ** 2 * 5) -> None:
        self._storage: t.Dict[str, TmpFile] = {}
        self._max_size = max_size

    async def write(self, path: str, data: t.IO[bytes]) -> None:
        file = TmpFile(max_size=self._max_size)
        await file.write(data.read())
        await file.seek(0)
        self._storage[path] = file

    async def exists(self, path: t.Union[str, PathLike]) -> bool:
        return path in self._storage

    async def read(self, path: str) -> FileReader:
        if path not in self._storage:
            raise FileNotFoundError('File not found: %s' % path)
        return self._storage[path]

    async def delete(self, path: str) -> None:
        if path in self._storage:
            del self._storage[path]
