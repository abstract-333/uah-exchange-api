import pytest

from src.redis_manager.redis_config import get_redis_config


@pytest.fixture(autouse=True)
@pytest.mark.anyio
async def clear_redis():
    redis = await get_redis_config()
    redis.flushall()
