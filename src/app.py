from typing import Final
import sentry_sdk
from arel import HotReloadMiddleware
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as aioredis, Redis
from redis.client import Redis
from starlette import status

from src.config import REDIS_SECRET_KEY
from src.routers import all_routers

# Adding sentry to save logs and exception in server
sentry_sdk.init(
    dsn="https://47e2e3bba7c79bc9509ffc9c4a32a278@o4505839140798464.ingest.sentry.io/4505839142109184",
    traces_sample_rate=1.0,
    profiles_sample_rate=1.0,
)

app = FastAPI(
    title="UAHRate",
    default_response_class=ORJSONResponse
)

# Adding hot reload middleware to make swagger ui changing dynamically
app.add_middleware(HotReloadMiddleware)


@app.exception_handler(Exception)
async def validation_exception_handler(request, err):
    """ Main exception handler for all routes,
        it returns if none of previous exceptions handlers catching anything"""
    base_error_message = f"Failed to execute: {request.method}: {request.url}"
    sentry_sdk.capture_message(f"{base_error_message}. Detail: {err}")
    return ORJSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "detail": "Internal Server Error"
        }
    )


@app.on_event("startup")
async def startup_event():
    # redis_manager: Redis
    redis: Final[Redis] = await aioredis.from_url(
        url=f"rediss://red-cjo66k358phs738s90fg:{REDIS_SECRET_KEY}@frankfurt-redis.render.com:6379",
        encoding="utf8",
        decode_responses=True
    )
    FastAPICache.init(backend=RedisBackend(redis), prefix="fastapi-cache")


@app.on_event("shutdown")
async def shutdown_event():
    # Clear fastapi cache when shutting down
    await FastAPICache.clear()


# Include all routers
for router in all_routers:
    app.include_router(router=router)
