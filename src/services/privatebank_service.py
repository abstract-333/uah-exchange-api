from typing import Final, List

from src.api.schemas import ExchangeRate, BankExchangeRate, InternationalCurrency
from src.core.repository import Repository
from src.core.urls import PRIVAT_BANK_ONLINE_URL, PRIVAT_BANK_CASH_URL
from src.core.service import Service
from src.redis_manager.repository import RedisRepository


class PrivatBankService(Service):
    bank_name: Final[str] = "PrivatBank"
    url_online: Final = PRIVAT_BANK_ONLINE_URL
    url_cash: Final = PRIVAT_BANK_CASH_URL
    request_repo: Final = Repository()
    redis_repo: Final = RedisRepository(name=bank_name)

    async def get_online_exchange_rate(self) -> BankExchangeRate | None:
        """Get online exchange rate in PrivatBank"""
        return await self._get_exchange_rate(self.url_online, exchange_type='online')

    async def get_cash_exchange_rate(self) -> BankExchangeRate | None:
        """Get cash exchange rate in PrivatBank"""
        return await self._get_exchange_rate(self.url_cash, exchange_type='cash')

    async def _get_exchange_rate(self, cash_or_online_url: str, exchange_type: str):
        status_code, response = await self.request_repo.get_request_json(url=cash_or_online_url)

        if status_code != 200:
            # If there is no date available form server, use cache
            cached_exchange_rate = await self.redis_repo.get_stored_data()
            return BankExchangeRate(**cached_exchange_rate)

        rates_list: list = await self._convert_dict_to_list(response)

        ordered_rates_list: list[ExchangeRate] | None = await self.set_first_appeared_currencies(
            unordered_list=rates_list,
            first_appeared_currency=self.first_appeared_currency,
            second_appeared_currency=self.second_appeared_currency
        )

        if ordered_rates_list is None:
            cached_exchange_rate = await self.redis_repo.get_stored_data(name_prefix=exchange_type)
            return BankExchangeRate(**cached_exchange_rate)

        returned_rate_bank = BankExchangeRate(
            bank_name=self.bank_name,
            rates=ordered_rates_list
        )
        await self.redis_repo.store_value(keys=returned_rate_bank.model_dump(), name_prefix=exchange_type)
        return returned_rate_bank

    @staticmethod
    async def _convert_dict_to_list(entered_list: List) -> list[ExchangeRate]:
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
