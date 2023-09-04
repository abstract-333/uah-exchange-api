import asyncio
import time
import httpx
from bs4 import BeautifulSoup
from fastapi import APIRouter, HTTPException
from fastapi_cache.decorator import cache
from pydantic import ValidationError
from starlette import status
from starlette.requests import Request
from starlette.responses import Response

from core.service import Service
from services.avalbank_service import AvalBankService
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
    response_model=list[BankExchangeRate | None],
    responses=get_exchange_rate_doc,
)
# @cache(expire=60 * 2)  # 2 minutes
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

        list_of_rates = await Service().execute_tasks(tasks)

        print(time.time() - start_time)
        return list_of_rates

    except TooManyRequests:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Too many requests"
        )

    except ValidationError as exc:
        print(repr(exc.errors()[0]['type']))


@online_rate_router.get(
    path='/cash/all',
    response_model=list[BankExchangeRate | None],
    responses=get_exchange_rate_doc
)
# @cache(expire=60 * 2)  # 2 minutes
async def get_cash_exchange_rate(
        request: Request,
        response: Response,
):
    try:
        start_time = time.time()

        banks_services = [PrivatBankService(), AvalBankService()]

        tasks = [
            bank_service.get_cash_exchange_rate() for bank_service in banks_services
        ]

        # Run the tasks concurrently
        results = await asyncio.gather(*tasks, return_exceptions=True)

        # Add all values that are not None
        list_of_rates = [element for element in results if element is not None]

        print(time.time() - start_time)
        return list_of_rates

    except TooManyRequests:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Too many requests"
        )


@online_rate_router.get(
    path='/aval',
    # response_model=list[BankExchangeRate | None],
    responses=get_exchange_rate_doc
)
# @cache(expire=60 * 2)  # 2 minutes
async def get_aval(
        request: Request,
        response: Response,
):
    try:
        start_time = time.time()
        url = 'https://raiffeisen.ua'  # URL to scrape
        # response = requests.get(url).text
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            soup = BeautifulSoup(response.text, 'lxml')
            print(soup)
            rates = soup.find_all("div", class_="bank-info__table-column")
            print(rates)
            # print(rates)
            # for rate in rates:
            #     if rate.text == "Райффайзен Банк Аваль":
            #         index_bank = rates.index(rate)
            #         print(time.time() - start_time)
            #         return {
            #             "Buy": rates[index_bank + 1].text,
            #             "Sell": rates[index_bank + 2].text
            #         }

    except TooManyRequests:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Too many requests"
        )
