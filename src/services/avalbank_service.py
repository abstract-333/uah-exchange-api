from abc import ABC
from typing import Final
from bs4 import BeautifulSoup

from src.api.schemas import (
    ExchangeRate,
    NationalCurrency,
    BankExchangeRate,
    InternationalCurrency,
    BanksAvailable,
)
from src.core.repository import Repository
from src.core.service import Service
from src.core.urls import AVAL_BANK_CASH_URL, OSCHAD_BANK_URL
from src.redis_manager.repository import RedisRepository
from src.utils.async_tasks import execute_tasks


class AvalBankService(Service, ABC):
    bank_name: Final[BanksAvailable] = BanksAvailable.aval_bank
    url_cash: Final[str] = AVAL_BANK_CASH_URL
    url_online: Final[str] = OSCHAD_BANK_URL
    request_repo: Final = Repository()
    redis_repo: Final = RedisRepository(name=bank_name)
    first_appeared_currency = InternationalCurrency.usd
    second_appeared_currency = InternationalCurrency.eur

    async def get_cash_exchange_rate(self) -> BankExchangeRate | None:
        """Get online exchange rate in Aval Bank"""

        # Generate tasks to asynchronously exchange rate for the first and second currencies
        tasks = [
            self._parse_cash_exchange_rate(
                currency_target=self.first_appeared_currency
            ),
            self._parse_cash_exchange_rate(
                currency_target=self.second_appeared_currency
            ),
        ]

        executed_tasks = await execute_tasks(tasks)

        if not executed_tasks:
            cached_exchange_rate = await self.redis_repo.get_stored_data()

            if cached_exchange_rate is None:
                return BankExchangeRate(bank_name=self.bank_name, rates=None)

            return BankExchangeRate(**cached_exchange_rate)

        returned_rate_bank = BankExchangeRate(
            bank_name=self.bank_name, rates=executed_tasks
        )

        await self.redis_repo.store_value(keys=returned_rate_bank.model_dump())

        return returned_rate_bank

    async def _parse_cash_exchange_rate(
        self, currency_target: InternationalCurrency
    ) -> ExchangeRate | None:
        """Get exchange rate for currency variable by parsing html web page"""
        status_code, page = await self.request_repo.get_request(
            url=self.url_cash + currency_target
        )

        # Return None if response is not success (not 200 status code)
        if status_code != 200:
            return None

        soup = BeautifulSoup(page.text, "lxml")

        rates = soup.find_all("div", class_="table-wrapper")[1].find_all("td")
        for rate in rates:
            if rate.text == "Райффайзен Банк Аваль":
                index_bank = rates.index(rate)
                return ExchangeRate(
                    first_currency=currency_target,
                    second_currency=NationalCurrency.uah,
                    buy=rates[index_bank + 1].text,
                    sell=rates[index_bank + 2].text,
                )
        return None
