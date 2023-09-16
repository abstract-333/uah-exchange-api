import time
from fastapi import APIRouter, HTTPException
from fastapi_cache.decorator import cache
from starlette import status
from starlette.requests import Request
from starlette.responses import Response
from src.services.pumb_bank_service import PumbBankService
from src.services.universlbank_service import UniversalBankService
from src.services.oschadbank_service import OschadBankService
from src.api.schemas import BankExchangeRate
from src.core.service import Service
from src.services.avalbank_service import AvalBankService
from src.services.centralbank_service import CentralBankService
from src.services.monobank_service import MonoBankService
from src.services.privatebank_service import PrivatBankService
from src.utils.async_tasks import execute_tasks

from src.core.dependencies import AllBanksServices
from src.utils.exceptions import TooManyRequests
from .docs import get_exchange_rate_doc
from .schemas import BankExchangeRate, BanksAvailable

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
        # await AvalBankService().parse_online_exchange_rate()
        print(time.time() - start_time)
        return list_of_rates

    except TooManyRequests:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Too many requests"
        )


@online_rate_router.get(
    path="/online/bank/",
    response_model=BankExchangeRate | None,
    # responses=get_exchange_rate_doc,
)
# @cache(expire=60 * 2)  # 2 minutes
async def get_online_exchange_rate(
        request: Request,
        response: Response,
        bank_requested: BanksAvailable
):
    try:
        start_time = time.time()

        print(time.time() - start_time)
        bank_service = eval(bank_requested + "Service")
        return await bank_service().get_online_exchange_rate()
        # return list_of_rates

    except TooManyRequests:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Too many requests"
        )


@online_rate_router.get(
    path="/cash/bank/",
    response_model=BankExchangeRate | None,
    # responses=get_exchange_rate_doc,
)
# @cache(expire=60 * 2)  # 2 minutes
async def get_online_exchange_rate(
        request: Request,
        response: Response,
        bank_requested: BanksAvailable
):
    try:
        start_time = time.time()

        print(time.time() - start_time)
        bank_service = eval(bank_requested + "Service")
        return await bank_service().get_cash_exchange_rate()
        # return list_of_rates

    except TooManyRequests:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Too many requests"
        )
