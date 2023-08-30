from typing import Final

from api.schemas import ExchangeRate
from core.repository import Repository
from core.urls import MONO_BANK_ONLINE
from utils.exceptions import TooManyRequests


class MonoBankService:
    url_online: Final = MONO_BANK_ONLINE
    repo = Repository()

    async def get_online_exchange_rate(self) -> dict[str, list]:
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
                buy=row["rateBuy"],
                sell=row["rateSell"]
            )
            for row in euro_dollar_response
        ]
        return {"monobank": exchange_rate_list}
