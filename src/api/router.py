import time
from fastapi import APIRouter, HTTPException
from fastapi_cache.decorator import cache
from starlette import status
from starlette.requests import Request
from starlette.responses import Response

from src.core.dependencies import AllBanksServices
from src.utils.exceptions import TooManyRequests
from .docs import get_exchange_rate_doc
from .schemas import BankExchangeRate

online_rate_router = APIRouter(
    prefix="/currency",
    tags=["All Banks"],
)


@online_rate_router.get(
    path='/online/all',
    response_model=list[BankExchangeRate | None],
    responses=get_exchange_rate_doc,
)
# @cache(expire=60 * 2)  # 2 minutes
async def get_online_exchange_rate(
        request: Request,
        response: Response,
        banks_service: AllBanksServices
):
    try:
        start_time = time.time()

        list_of_rates = await banks_service.get_online_exchange_rate()

        print(time.time() - start_time)
        return list_of_rates

    except TooManyRequests:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Too many requests"
        )


@online_rate_router.get(
    path='/cash/all',
    response_model=list[BankExchangeRate | None],
    responses=get_exchange_rate_doc,
)
# @cache(expire=60 * 2)  # 2 minutes
async def get_cash_exchange_rate(
        request: Request,
        response: Response,
        banks_service: AllBanksServices
):
    try:
        start_time = time.time()

        list_of_rates = await banks_service.get_cash_exchange_rate()

        print(time.time() - start_time)
        return list_of_rates
    except TooManyRequests:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Too many requests"
        )
