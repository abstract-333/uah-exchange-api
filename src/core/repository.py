from typing import Any
import httpx


class Repository:
    @staticmethod
    async def get_request(url: str) -> (int, Any):
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            status_code = response.status_code

            if status_code != 200:
                return status_code, response.headers

            return status_code, response.json()

