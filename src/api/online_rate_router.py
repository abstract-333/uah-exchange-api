from fastapi import APIRouter, HTTPException, Depends
from fastapi_cache.decorator import cache
from starlette import status
from starlette.requests import Request
from starlette.responses import Response

from limiter.limiter import BucketLimiter
from .docs import get_cash_exchange_rate_doc
from services.monobank_service import MonoBankService
from utils.exceptions import TooManyRequests

online_rate_router = APIRouter(
    prefix="/exchange-rate",
    tags=["All Banks"],
)


@online_rate_router.get(
    path='/cash',
    dependencies=[Depends(BucketLimiter())],
    responses=get_cash_exchange_rate_doc
)
@cache(expire=60)  # 1 minute
async def get_cash_exchange_rate(
        request: Request,
        response: Response,
):
    try:
        print("get logged")
        monobank_exchange_online = await MonoBankService().get_online_exchange_rate()

        return monobank_exchange_online

    except TooManyRequests:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Too many requests"
        )

    # except Exception:
    #     raise HTTPException(
    #         status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
    #     )
    #
