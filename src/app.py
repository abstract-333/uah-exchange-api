from fastapi import FastAPI, Depends
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as aioredis
from starlette.responses import JSONResponse
from routers import all_routers

app = FastAPI(
    title="UAHRate",
    # dependencies=[Depends(BucketLimiter(
    #     rate_unauthenticated=25,
    #     time_unauthenticated=60,
    # ))]
)


@app.exception_handler(Exception)
async def validation_exception_handler(request, err):
    """ Main exception handler for all routes,
        it returns if none of previous exceptions handlers catching anything"""
    base_error_message = f"Failed to execute: {request.method}: {request.url}"
    # Change here to LOGGER
    return JSONResponse(
        status_code=500,
        content={"message": f"{base_error_message}. Detail: {err}"}
    )


@app.on_event("startup")
async def startup_event():
    redis = aioredis.from_url(url="redis://localhost:6379", encoding="utf8", decode_responses=True)
    FastAPICache.init(backend=RedisBackend(redis), prefix="fastapi-cache")


@app.on_event("shutdown")
async def shutdown_event():
    await FastAPICache.clear(namespace="fastapi-cache")


for router in all_routers:
    app.include_router(router=router)
