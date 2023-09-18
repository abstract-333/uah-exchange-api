import asyncio

import uvicorn

from src.settings import settings


async def main():
    if __name__ == "__main__":
        uvicorn.run(
            "src.app:app",
            log_level="info",
            host=settings.server_host,
            port=settings.server_port,
            reload=True,
        )


asyncio.run(main())
