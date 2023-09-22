from typing import Final

from bs4 import BeautifulSoup

from src.api.schemas import InternationalCurrency
from src.api.schemas import BankExchangeRate, ExchangeRate, NationalCurrency
from src.core.repository import Repository
from src.core.service import Service
from src.core.urls import OSCHAD_BANK_URL
from src.redis_manager.repository import RedisRepository


class OschadBankService(Service):
    bank_name: Final[str] = "OschadBank"
    url_cash: Final[str] = OSCHAD_BANK_URL
    request_repo: Final = Repository()
    redis_repo: Final = RedisRepository(name=bank_name)
    first_appeared_currency = InternationalCurrency.usd
    second_appeared_currency = InternationalCurrency.eur

    async def get_cash_exchange_rate(self) -> BankExchangeRate | None:
        status_code, page = await self.request_repo.get_request(url=self.url_cash)
        if status_code != 200:
            # If there is no date available form server, use cache
            cached_exchange_rate = await self.redis_repo.get_stored_data()

            if cached_exchange_rate is None:
                return BankExchangeRate(bank_name=self.bank_name, rates=None)

            return BankExchangeRate(**cached_exchange_rate)

        returned_rate_bank = await self._get_exchange_rate_parsing(page.text)

        await self.redis_repo.store_value(keys=returned_rate_bank.model_dump())
        return returned_rate_bank

    async def _get_exchange_rate_parsing(self, page) -> BankExchangeRate:
        index_base = 36

        soup = BeautifulSoup(page, "lxml")
        rates_buy = soup.find_all("span", class_="item-rate")
        rates_sell = soup.find_all("span", class_="item-total")
        list_of_rates = []
        for iteration in range(2):
            current_currency: InternationalCurrency = InternationalCurrency.usd

            if iteration == 1:
                current_currency = InternationalCurrency.eur

            exchange_rate = ExchangeRate(
                first_currency=current_currency,
                second_currency=NationalCurrency.uah,
                buy=str.strip(rates_buy[index_base + iteration].text),  # type: ignore
                sell=str.strip(rates_sell[index_base + iteration].text),  # type: ignore
            )
            list_of_rates.append(exchange_rate)
        returned_rate_bank = BankExchangeRate(
            bank_name=self.bank_name, rates=list_of_rates
        )
        return returned_rate_bank
