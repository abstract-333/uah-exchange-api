from fastapi import FastAPI, Depends
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as aioredis

from routers import all_routers

app = FastAPI(
    title="UAHRate",
    # dependencies=[Depends(BucketLimiter())]
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
