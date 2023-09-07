import pytest
from redis import asyncio as aioredis, Redis
from settings import settings


@pytest.fixture(scope="session", autouse=True)
async def setup_redis():
    assert settings.mode == "TEST"
    redis: Redis = await aioredis.from_url(
        url=settings.redis_url(), encoding="utf8",
        decode_responses=True
    )
    redis.flushall(asynchronous=True)
