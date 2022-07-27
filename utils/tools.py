from pathlib import Path

from aiofiles import open as aioopen
from aiohttp import ClientSession


async def download(url: str, filepath: str | Path, session: ClientSession) -> Path:
    async with session.get(url) as response:
        async with aioopen(filepath, "wb") as file:
            async for chunk in response.content.iter_chunked(4096):
                await file.write(chunk)
    return Path(filepath)
