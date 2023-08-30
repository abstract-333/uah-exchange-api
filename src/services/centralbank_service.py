from typing import Final

from api.schemas import ExchangeRate, InternationalCurrency, NationalCurrency
from core.repository import Repository
from core.urls import CENTRAL_BANK_ONLINE
from core.service import Service
from utils.exceptions import TooManyRequests


class CentralBankService(Service):
    url_online: Final = CENTRAL_BANK_ONLINE
    repo: Final = Repository()
    first_appeared_currency: Final = InternationalCurrency.usd
    second_appeared_currency: Final = InternationalCurrency.eur

    async def get_online_exchange_rate(self) -> dict[str, list]:
        """Get online exchange rate in Central Bank of Ukraine (NBU)"""
        status_code, response = await self.repo.get_request(url=self.url_online)

        if status_code == 429:
            raise TooManyRequests

        exchange_rate_list = []
        for row in response:
            if row["cc"] in (InternationalCurrency.usd, InternationalCurrency.eur):
                exchange_rate_row = ExchangeRate(
                    first_currency=row["cc"],
                    second_currency=NationalCurrency.uah,
                    buy=row["rate"],
                    sell=row["rate"]
                )
                exchange_rate_list.append(exchange_rate_row)

        ordered_rates_list: list = await self.set_two_first_appeared(
            unordered_list=exchange_rate_list,
            first_appeared_currency=self.first_appeared_currency,
            second_appeared_currency=self.second_appeared_currency
        )

        return {"CentralBank": ordered_rates_list}

