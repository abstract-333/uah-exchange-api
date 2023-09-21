from typing import Final

from redis import asyncio as aioredis, Redis
from src.settings import settings


async def get_redis_config() -> Redis:
    redis: Final[Redis] = await aioredis.from_url(  # type: ignore
        url=f"redis://{settings.redis_host}:{settings.redis_port}",
        encoding="utf8",
        decode_responses=True,
    )
    return redis
