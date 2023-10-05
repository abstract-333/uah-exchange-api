from typing import Final

from src.api.schemas import (
    ExchangeRate,
    InternationalCurrency,
    NationalCurrency,
    BankExchangeRate,
    BanksAvailable,
)
from src.core.repository import Repository
from src.core.service import Service, set_first_appeared_currencies
from src.core.urls import MONO_BANK_ONLINE_URL
from src.redis_manager.repository import RedisRepository


class MonoBankService(Service):
    bank_name: Final[BanksAvailable] = BanksAvailable.mono_bank
    url_online: Final = MONO_BANK_ONLINE_URL
    request_repo: Final = Repository()
    redis_repo: Final = RedisRepository(name=bank_name)
    first_appeared_currency = InternationalCurrency.usd
    second_appeared_currency = InternationalCurrency.eur

    async def get_online_exchange_rate(self) -> BankExchangeRate | None:
        """Get online exchange rate in MonoBank"""
        status_code, response = await self.request_repo.get_request(url=self.url_online)

        if status_code != 200:
            # If there is no date available form server, use cache
            cached_exchange_rate = await self.redis_repo.get_stored_data()

            if cached_exchange_rate is None:
                return BankExchangeRate(bank_name=self.bank_name, rates=None)

            return BankExchangeRate(**cached_exchange_rate)

        euro_dollar_response = response.json()[:2]
        exchange_rate_list = [
            ExchangeRate(
                first_currency=InternationalCurrency.usd
                if row["currencyCodeA"] == 840
                else InternationalCurrency.eur,
                second_currency=NationalCurrency.uah,
                date=str(row["date"]),
                buy=row["rateBuy"],
                sell=row["rateSell"],
            )
            for row in euro_dollar_response
        ]
        ordered_rates_list: list[
            ExchangeRate
        ] | None = await set_first_appeared_currencies(
            unordered_list=exchange_rate_list,
            first_appeared_currency=self.first_appeared_currency,
            second_appeared_currency=self.second_appeared_currency,
        )
        if ordered_rates_list is None:
            cached_exchange_rate = await self.redis_repo.get_stored_data()

            return BankExchangeRate(**cached_exchange_rate)

        returned_rate_bank = BankExchangeRate(
            bank_name=self.bank_name, rates=ordered_rates_list
        )

        await self.redis_repo.store_value(keys=returned_rate_bank.model_dump())

        return returned_rate_bank
