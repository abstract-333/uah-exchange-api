from typing import Final

from src.api.schemas import (
    ExchangeRate,
    InternationalCurrency,
    NationalCurrency,
    BankExchangeRate,
    BanksAvailable,
)
from src.core.repository import Repository
from src.core.urls import CENTRAL_BANK_ONLINE_URL
from src.core.service import Service, set_first_appeared_currencies
from src.redis_manager.repository import RedisRepository


class CentralBankService(Service):
    bank_name: Final[BanksAvailable] = BanksAvailable.central_bank
    url_online: Final = CENTRAL_BANK_ONLINE_URL
    request_repo: Final = Repository()
    redis_repo: Final = RedisRepository(name=bank_name)

    first_appeared_currency = InternationalCurrency.usd
    second_appeared_currency = InternationalCurrency.eur

    async def get_online_exchange_rate(self) -> BankExchangeRate | None:
        """Get online exchange rate in Central Bank of Ukraine (NBU)"""
        status_code, response = await self.request_repo.get_request(url=self.url_online)

        if status_code != 200:
            # If there is no date available form server, use cache
            cached_exchange_rate = await self.redis_repo.get_stored_data()

            if cached_exchange_rate is None:
                return BankExchangeRate(bank_name=self.bank_name, rates=None)

            return BankExchangeRate(**cached_exchange_rate)

        exchange_rate_list = []
        for row in response.json():
            if row["cc"] in (InternationalCurrency.usd, InternationalCurrency.eur):
                exchange_rate_row = ExchangeRate(
                    first_currency=row["cc"],
                    second_currency=NationalCurrency.uah,
                    buy=row["rate"],
                    sell=row["rate"],
                )
                exchange_rate_list.append(exchange_rate_row)

        ordered_rates_list: list[
            ExchangeRate
        ] | None = await set_first_appeared_currencies(
            unordered_list=exchange_rate_list,
            first_appeared_currency=self.first_appeared_currency,
            second_appeared_currency=self.second_appeared_currency,
        )

        if ordered_rates_list is not None:
            returned_rate_bank = BankExchangeRate(
                bank_name=self.bank_name, rates=ordered_rates_list
            )
            await self.redis_repo.store_value(keys=returned_rate_bank.model_dump())

            return returned_rate_bank

        cached_exchange_rate = await self.redis_repo.get_stored_data()

        if cached_exchange_rate is None:
            return BankExchangeRate(bank_name=self.bank_name, rates=None)

        return BankExchangeRate(**cached_exchange_rate)
