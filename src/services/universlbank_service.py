from typing import Final

from bs4 import BeautifulSoup

from src.api.schemas import ExchangeRate, NationalCurrency, BankExchangeRate, InternationalCurrency
from src.core.repository import Repository
from src.core.service import Service
from src.core.urls import UNIVERSAL_BANK_CASH_URL
from src.redis_manager.repository import RedisRepository


class UniversalBankService(Service):
    bank_name: Final[str] = "UniversalBank"
    url_cash_online: Final[str] = UNIVERSAL_BANK_CASH_URL
    request_repo: Final = Repository()
    redis_repo: Final = RedisRepository(name=bank_name)

    async def get_cash_exchange_rate(self) -> BankExchangeRate | None:
        status_code, page = await self.request_repo.get_request_text(url=self.url_cash_online)

        if status_code != 200:
            # If there is no date available form server, use cache
            cached_exchange_rate = await self.redis_repo.get_stored_data()
            return BankExchangeRate(**cached_exchange_rate)

        returned_rate_bank = await self._get_cash_online_parsing(page)

        await self.redis_repo.store_value(keys=returned_rate_bank.model_dump())
        return returned_rate_bank

    async def _get_cash_online_parsing(self, page) -> BankExchangeRate:

        index_base = 4

        soup = BeautifulSoup(page, 'lxml')
        rates = soup.find_all("td", class_="p-b-xs-2 p-y-1-sm")
        list_of_rates = []
        for iteration in range(2):

            current_currency: InternationalCurrency = InternationalCurrency.usd
            if iteration == 1:
                current_currency = InternationalCurrency.eur

            exchange_rate = ExchangeRate(
                first_currency=current_currency,
                second_currency=NationalCurrency.uah,
                buy=str.strip(rates[index_base + iteration * 6].text),  # type: ignore
                sell=str.strip(rates[index_base + 1 + iteration * 6].text)  # type: ignore
            )

            list_of_rates.append(exchange_rate)

        returned_rate_bank = BankExchangeRate(
            bank_name=self.bank_name,
            rates=list_of_rates
        )
        return returned_rate_bank
