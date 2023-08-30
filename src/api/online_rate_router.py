from fastapi import APIRouter, HTTPException
from starlette import status
from starlette.requests import Request
from starlette.responses import Response
from services.privatebank_service import PrivatBankService
from .docs import get_exchange_rate_doc
from services.monobank_service import MonoBankService
from utils.exceptions import TooManyRequests
from .schemas import ExchangeRate

online_rate_router = APIRouter(
    prefix="/currency",
    tags=["All Banks"],
)


@online_rate_router.get(
    path='/online/all',
    response_model=list[dict[str, list[ExchangeRate]]],
    responses=get_exchange_rate_doc,
)
# @cache(expire=60)  # 1 minute
async def get_online_exchange_rate(
        request: Request,
        response: Response,
):
    try:
        list_of_rates = []
        privatbank_exchange_online: dict = await PrivatBankService().get_online_exchange_rate()
        monobank_exchange_online: dict = await MonoBankService().get_online_exchange_rate()

        list_of_rates.append(privatbank_exchange_online)
        list_of_rates.append(monobank_exchange_online)

        return list_of_rates

    except TooManyRequests:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Too many requests"
        )


@online_rate_router.get(
    path='/cash/all',
    response_model=list[dict[str, list[ExchangeRate]]],
    responses=get_exchange_rate_doc
)
# @cache(expire=60)  # 1 minute
async def get_cash_exchange_rate(
        request: Request,
        response: Response,
):
    try:
        list_of_rates = []
        privatbank_exchange_online: dict = await PrivatBankService().get_cash_exchange_rate()

        list_of_rates.append(privatbank_exchange_online)

        return list_of_rates

    except TooManyRequests:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Too many requests"
        )


