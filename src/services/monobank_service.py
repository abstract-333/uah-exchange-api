from typing import Final

from api.schemas import ExchangeRate, InternationalCurrency, NationalCurrency, BankExchangeRate
from core.repository import Repository
from core.service import Service
from core.urls import MONO_BANK_ONLINE_URL
from redis_manager.repository import RedisRepository


class MonoBankService(Service):
    url_online: Final = MONO_BANK_ONLINE_URL
    request_repo: Final = Repository()
    redis_repo: Final = RedisRepository(name="MonoBank")
    first_appeared_currency: Final = InternationalCurrency.usd
    second_appeared_currency: Final = InternationalCurrency.eur

    async def get_online_exchange_rate(self) -> BankExchangeRate | None:
        """Get online exchange rate in MonoBank"""
        status_code, response = await self.request_repo.get_request_json(url=self.url_online)

        if status_code == 429:
            # If there is no date available form server, use cache
            cached_exchange_rate = await self.redis_repo.get_stored_data()
            return BankExchangeRate(**cached_exchange_rate)

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
        returned_rate_bank = BankExchangeRate(
            bank_name="MonoBank",
            rates=ordered_rates_list
        )

        await self.redis_repo.store_value(keys=returned_rate_bank.model_dump())

        return returned_rate_bank


