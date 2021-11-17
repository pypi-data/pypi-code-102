from __future__ import annotations

import io
import typing as t
from os import PathLike

from .drivers.base import Driver
from .protocols import FileReader


class File:
    def __init__(self, reader: FileReader, mode: str) -> None:
        self._reader = reader
        self._mode = mode

    async def read(self, size: int = -1) -> t.Union[str, bytes]:
        chunk = await self._reader.read(size)
        if 'b' in self._mode:
            return chunk
        return chunk.decode()

    async def __aenter__(self) -> File:
        await self._reader.__aenter__()
        return self

    async def __aexit__(self, *args: t.Any) -> None:
        await self._reader.__aexit__(*args)


class Storage:
    _driver_map: t.Dict[str, str] = {
        'local': 'deesk.drivers.fs.LocalFsDriver',
        'memory': 'deesk.drivers.memory.MemoryDriver',
        's3': 'deesk.drivers.s3.S3Driver',
    }

    def __init__(self, driver: Driver) -> None:
        self._driver = driver

    async def get(self, path: t.Union[str, PathLike], mode: str = 'rb') -> File:
        return File(await self._driver.read(str(path)), mode)

    async def put(self, path: t.Union[str, PathLike], data: t.Union[str, bytes, t.IO[bytes]]) -> None:
        if isinstance(data, str):
            data = data.encode()

        if isinstance(data, bytes):
            data = io.BytesIO(data)

        return await self._driver.write(str(path), data)

    async def delete(self, path: t.Union[str, PathLike]) -> None:
        return await self._driver.delete(str(path))

    async def exists(self, path: t.Union[str, PathLike]) -> bool:
        return await self._driver.exists(str(path))

    async def missing(self, path: str) -> bool:
        return not await self._driver.exists(path)

    # async def copy(self, path: str, new_path: str) -> None:
    #     return not await self._driver.copy(path, new_path)
    #
    # async def move(self, path: str, new_path: str) -> None:
    #     return not await self._driver.move(path, new_path)
    #
    # async def link(self, path: str, new_path: str) -> None:
    #     return not await self._driver.link(path, new_path)
    #
    # async def create_dir(self, path: str) -> None: ...
    #
    # async def delete_dir(self, path: str) -> None: ...
    #
    # async def list_dir(self, path: str) -> None: ...
    #
    # async def last_modified(self, path: str) -> None: ...
    #
    # async def mime_type(self, path: str) -> None: ...
    #
    # async def size(self, path: str) -> None: ...
