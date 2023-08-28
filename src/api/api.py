import httpx
from fastapi import APIRouter

from core.urls import MONO_BANK_ONLINE

cash_router = APIRouter(
    prefix="/exchange-rate",
    tags=["Cash"]
)


@cash_router.get('')
async def get_cash_exchange_rate():
    async with httpx.AsyncClient() as client:
        response = await client.get(MONO_BANK_ONLINE)
        if response.status_code == 200:
            return response.json()[:2]


