from typing import Final

from api.schemas import ExchangeRate, InternationalCurrency, NationalCurrency, BankExchangeRate
from core.repository import Repository
from core.urls import CENTRAL_BANK_ONLINE_URL
from core.service import Service
from redis_manager.repository import RedisRepository


class CentralBankService(Service):
    url_online: Final = CENTRAL_BANK_ONLINE_URL
    request_repo: Final = Repository()
    redis_repo: Final = RedisRepository(name="CentralBank")
    first_appeared_currency: Final = InternationalCurrency.usd
    second_appeared_currency: Final = InternationalCurrency.eur

    async def get_online_exchange_rate(self) -> BankExchangeRate | None:
        """Get online exchange rate in Central Bank of Ukraine (NBU)"""
        status_code, response = await self.request_repo.get_request_json(url=self.url_online)

        if status_code == 429:
            # If there is no date available form server, use cache
            cached_exchange_rate = await self.redis_repo.get_stored_data()
            return BankExchangeRate(**cached_exchange_rate)

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
        returned_rate_bank = BankExchangeRate(
            bank_name="CentralBank",
            rates=ordered_rates_list
        )

        await self.redis_repo.store_value(keys=returned_rate_bank.model_dump())

        return returned_rate_bank
