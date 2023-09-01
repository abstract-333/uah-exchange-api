import asyncio
import time
from fastapi import APIRouter, HTTPException
from fastapi_cache.decorator import cache
from starlette import status
from starlette.requests import Request
from starlette.responses import Response

from services.centralbank_service import CentralBankService
from services.monobank_service import MonoBankService
from services.privatebank_service import PrivatBankService
from utils.exceptions import TooManyRequests
from .docs import get_exchange_rate_doc
from .schemas import BankExchangeRate

online_rate_router = APIRouter(
    prefix="/currency",
    tags=["All Banks"],
)


@online_rate_router.get(
    path='/online/all',
    response_model=list[BankExchangeRate],
    responses=get_exchange_rate_doc,
)
@cache(expire=60 * 2)  # 2 minutes
async def get_online_exchange_rate(
        request: Request,
        response: Response,
):
    try:
        start_time = time.time()

        banks = [CentralBankService(), PrivatBankService(), MonoBankService()]

        tasks = [
            bank_service.get_online_exchange_rate() for bank_service in banks
        ]

        # Run the tasks concurrently
        results = await asyncio.gather(*tasks, return_exceptions=True)

        list_of_rates = []
        list_of_rates.extend(results)

        print(time.time() - start_time)
        return list_of_rates

    except TooManyRequests:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Too many requests"
        )


@online_rate_router.get(
    path='/cash/all',
    response_model=list[BankExchangeRate],
    responses=get_exchange_rate_doc
)
@cache(expire=60 * 2)  # 2 minutes
async def get_cash_exchange_rate(
        request: Request,
        response: Response,
):
    try:
        start_time = time.time()

        banks_services = [PrivatBankService()]

        tasks = [
            bank_service.get_online_exchange_rate() for bank_service in banks_services
        ]

        # Run the tasks concurrently
        results = await asyncio.gather(*tasks, return_exceptions=True)

        list_of_rates = []
        list_of_rates.extend(results)

        print(time.time() - start_time)
        return list_of_rates

    except TooManyRequests:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Too many requests"
        )

