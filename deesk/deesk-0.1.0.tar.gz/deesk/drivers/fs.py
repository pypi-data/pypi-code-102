import anyio
import typing as t
from os import PathLike

from ..protocols import FileReader
from .base import Driver


class LocalFsDriver(Driver):
    def __init__(self, base_dir: t.Union[str, PathLike] = "/") -> None:
        self._base_path = anyio.Path(base_dir)

    async def write(self, path: str, data: t.IO[bytes]) -> None:
        resolved = await self._get_full_path(path)
        await resolved.parent.mkdir(parents=True, exist_ok=True)
        async with await anyio.open_file(resolved, 'wb') as f:
            await f.write(data.read())

    async def read(self, path: str) -> FileReader:
        resolved = await self._get_full_path(path)
        return await anyio.open_file(resolved, 'rb')

    async def delete(self, path: str) -> None:
        resolved = await self._get_full_path(path)
        return await resolved.unlink(True)

    async def exists(self, path: str) -> bool:
        resolved = await self._get_full_path(path)
        return await resolved.exists()

    async def _get_full_path(self, path: str) -> anyio.Path:
        resolved = await (self._base_path / path).absolute()
        if not str(resolved).startswith(str(self._base_path)):
            raise ValueError('Path does not belong to configured base directory "%s"' % self._base_path)
        return resolved
