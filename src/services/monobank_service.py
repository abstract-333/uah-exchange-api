from fastapi_cache.decorator import cache

from api.schemas import ExchangeRate
from core.repository import Repository
from core.urls import MONO_BANK_ONLINE
from utils.exceptions import TooManyRequests


class MonoBankService:
    url_online = MONO_BANK_ONLINE
    repo = Repository()

    async def get_online_exchange_rate(self):
        """Get online exchange rate in monobank"""
        status_code, response = await self.repo.get_request(url=self.url_online)

        if status_code == 429:
            raise TooManyRequests

        euro_dollar_response = response[:2]
        exchange_rate_list = [
            ExchangeRate(
                first_currency="USD" if row["currencyCodeA"] == 840 else "EUR",
                second_currency="UAH",
                date=str(row["date"]),
                rate_buy_first=row["rateBuy"],
                rate_sell_first=row["rateSell"]
            )
            for row in euro_dollar_response
]
        return exchange_rate_list