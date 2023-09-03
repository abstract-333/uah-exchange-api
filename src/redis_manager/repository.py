import json
from typing import Any, Final
from redis_manager.redis_config import get_redis_config


class RedisRepository:

    def __init__(self, name: str):
        self.name: Final[str] = name

    async def store_value(self, keys: Any) -> None:
        redis_storage = await get_redis_config()

        # Store data as json in redis_storage that will be expired in one day
        status_of_storing = await redis_storage.set(name=self.name, value=json.dumps(keys), ex=60 * 60 * 24)

        # Attempt to store the value until it will be success
        while status_of_storing is not True:
            status_of_storing = await redis_storage.set(name=self.name, value=keys, ex=60 * 60 * 24)

        return None

    async def get_stored_data(self) -> Any:
        """Get stored data in redis_storage"""
        redis_storage = await get_redis_config()

        value = await redis_storage.get(name=self.name)

        # Convert date that are stored as json to its primitive form
        return json.loads(value)
