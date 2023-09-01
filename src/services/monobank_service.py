from typing import Final

from api.schemas import ExchangeRate, InternationalCurrency, NationalCurrency, BankExchangeRate
from core.repository import Repository
from core.urls import MONO_BANK_ONLINE
from core.service import Service
from utils.exceptions import TooManyRequests


class MonoBankService(Service):
    url_online: Final = MONO_BANK_ONLINE
    repo: Final = Repository()
    first_appeared_currency: Final = InternationalCurrency.usd
    second_appeared_currency: Final = InternationalCurrency.eur

    async def get_online_exchange_rate(self) -> BankExchangeRate:
        """Get online exchange rate in MonoBank"""

        status_code, response = await self.repo.get_request(url=self.url_online)

        if status_code == 429:
            raise TooManyRequests

        euro_dollar_response = response[:2]
        exchange_rate_list = [
            ExchangeRate(
                first_currency=InternationalCurrency.usd if row["currencyCodeA"] == 840 else InternationalCurrency.eur,
                second_currency=NationalCurrency.uah,
                date=str(row["date"]),
                buy=row["rateBuy"],
                sell=row["rateSell"]
            )
            for row in euro_dollar_response
        ]
        ordered_rates_list: list = await self.set_two_first_appeared(
            unordered_list=exchange_rate_list,
            first_appeared_currency=self.first_appeared_currency,
            second_appeared_currency=self.second_appeared_currency
        )

        return BankExchangeRate(
            bank_name="MonoBank",
            rates=ordered_rates_list
        )
