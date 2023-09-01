from typing import Final, List

from api.schemas import ExchangeRate, InternationalCurrency, BankExchangeRate
from core.repository import Repository
from core.urls import PRIVAT_BANK_ONLINE, PRIVAT_BANK_CASH
from core.service import Service
from utils.exceptions import TooManyRequests


class PrivatBankService(Service):
    url_online: Final = PRIVAT_BANK_ONLINE
    url_cash: Final = PRIVAT_BANK_CASH
    repo: Final = Repository()
    first_appeared_currency: Final = InternationalCurrency.usd
    second_appeared_currency: Final = InternationalCurrency.eur

    async def get_online_exchange_rate(self) -> BankExchangeRate:
        """Get online exchange rate in PrivatBank"""
        status_code, response = await self.repo.get_request(url=self.url_online)

        if status_code == 429:
            raise TooManyRequests

        rates_list: list = await self.convert_dict_to_list(response)
        ordered_rates_list: list = await self.set_two_first_appeared(
            unordered_list=rates_list,
            first_appeared_currency=self.first_appeared_currency,
            second_appeared_currency=self.second_appeared_currency
        )

        return BankExchangeRate(
            bank_name="PrivatBank",
            rates=ordered_rates_list
        )

    async def get_cash_exchange_rate(self) -> BankExchangeRate:
        """Get cash exchange rate in PrivatBank"""
        status_code, response = await self.repo.get_request(url=self.url_cash)

        if status_code == 429:
            raise TooManyRequests

        rates_list: list = await self.convert_dict_to_list(response)

        ordered_rates_list: list = await self.set_two_first_appeared(
            unordered_list=rates_list,
            first_appeared_currency=self.first_appeared_currency,
            second_appeared_currency=self.second_appeared_currency
        )

        return BankExchangeRate(
            bank_name="PrivatBank",
            rates=ordered_rates_list
        )

    @staticmethod
    async def convert_dict_to_list(entered_list: List) -> list[ExchangeRate]:
        exchange_rate_list = [
            ExchangeRate(
                first_currency=row["ccy"],
                second_currency=row["base_ccy"],
                buy=row["buy"],
                sell=row["sale"]
            )
            for row in entered_list
        ]
        return exchange_rate_list
