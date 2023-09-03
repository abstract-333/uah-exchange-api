import json
from typing import Final, Any

from redis import asyncio as aioredis, Redis


async def get_redis_config():
    redis: Final[Redis] = await aioredis.from_url(
        url="redis://localhost:6379",
        encoding="utf8",
        decode_responses=True
    )
    return redis


