import time
from typing import Any, Tuple
import httpx


class Repository:
    @staticmethod
    async def get_request_json(url: str) -> Tuple[int, Any]:
        start_time = time.time()
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(url)
                status_code = response.status_code

                print(time.time() - start_time)
                if status_code != 200:
                    return status_code, response.json()
                return status_code, response.json()
        except httpx.RequestError:
            return 503, None

    @staticmethod
    async def get_request_text(url: str) -> Tuple[int, Any]:
        start_time = time.time()
        try:
            async with httpx.AsyncClient() as client:
                timeout = httpx.Timeout(10.0, connect=10.0, read=10.0, pool=10.0)
                response = await client.get(url, timeout=timeout)
                status_code = response.status_code

                print(time.time() - start_time)
                if status_code != 200:
                    return status_code, response.json()
                return status_code, response.text

        except httpx.RequestError:
            return 503, None
