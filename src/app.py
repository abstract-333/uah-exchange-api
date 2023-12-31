from typing import Final
import sentry_sdk
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis import Redis
from redis.client import Redis
from starlette import status

import settings
from src.redis_manager.redis_config import get_redis_config
from src.routers import all_routers

# Adding sentry to save logs and exception in server
sentry_sdk.init(
    dsn=settings.settings.sentry_api_key,
    traces_sample_rate=1.0,
    profiles_sample_rate=1.0,
)

app = FastAPI(title="UAHRate", default_response_class=ORJSONResponse)

# Adding hot reload middleware to make swagger ui changing dynamically
# app.add_middleware(HotReloadMiddleware)


@app.exception_handler(Exception)
async def validation_exception_handler(request, err):
    """Main exception handler for all routes,
    it returns if none of previous exceptions handlers catching anything"""
    base_error_message = f"Failed to execute: {request.method}: {request.url}"
    sentry_sdk.capture_message(f"{base_error_message}. Detail: {err}")
    return ORJSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "Internal Server Error"},
    )


@app.on_event("startup")
async def startup_event():
    # redis_manager: Redis
    redis: Final[Redis] = await get_redis_config()
    FastAPICache.init(backend=RedisBackend(redis), prefix="fastapi-cache")


@app.on_event("shutdown")
async def shutdown_event():
    # Clear fastapi cache when shutting down
    await FastAPICache.clear()


# Include all routers
for router in all_routers:
    app.include_router(router=router)
