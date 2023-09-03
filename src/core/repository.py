import time
from typing import Any
import httpx


class Repository:
    @staticmethod
    async def get_request(url: str) -> (int, Any):
        start_time = time.time()
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            status_code = response.status_code

            print(time.time() - start_time)
            if status_code != 200:
                return status_code, response.json()
            return status_code, response.json()
