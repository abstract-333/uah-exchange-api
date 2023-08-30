import time
from datetime import datetime
from typing import Final, List, Any, Coroutine, Dict

from api.schemas import ExchangeRate
from core.repository import Repository
from core.urls import PRIVAT_BANK_ONLINE, PRIVAT_BANK_CASH
from utils.exceptions import TooManyRequests


class PrivatBankService:
    url_online: Final = PRIVAT_BANK_ONLINE
    url_cash: Final = PRIVAT_BANK_CASH
    repo = Repository()

    async def get_online_exchange_rate(self) -> dict[str, list]:
        """Get online exchange rate in privatebank"""
        status_code, response = await self.repo.get_request(url=self.url_online)

        if status_code == 429:
            raise TooManyRequests

        rates_list: list = await self.convert_dict_to_list_pydantic(response)
        return {"privatbank": rates_list}

    async def get_cash_exchange_rate(self) -> dict[str, list]:
        """Get cash exchange rate in privatebank"""
        status_code, response = await self.repo.get_request(url=self.url_cash)

        if status_code == 429:
            raise TooManyRequests

        rates_list: list = await self.convert_dict_to_list_pydantic(response)
        return {"privatbank": rates_list}

    async def convert_dict_to_list_pydantic(self, entered_list: List) -> list[ExchangeRate]:
        exchange_rate_list = [
            ExchangeRate(
                first_currency=row["ccy"],
                second_currency=row["base_ccy"],
                date=str(int(time.time())),
                buy=row["buy"],
                sell=row["sale"]
            )
            for row in entered_list
        ]
        return exchange_rate_list
