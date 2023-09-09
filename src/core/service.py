import asyncio
from typing import Any

from src.api.schemas import InternationalCurrency, BankExchangeRate


class Service:
    first_appeared_currency: InternationalCurrency
    second_appeared_currency: InternationalCurrency

    async def get_online_exchange_rate(self):
        ...

    async def get_cash_exchange_rate(self):
        ...

    @staticmethod
    async def set_first_appeared_currencies(
            unordered_list: list[Any],
            first_appeared_currency: str,
            second_appeared_currency: str
    ) -> list[Any] | None:

        for index_rate in range(len(unordered_list) - 1):

            if unordered_list[index_rate].first_currency == first_appeared_currency and index_rate != 0:
                unordered_list[index_rate], unordered_list[0] = (
                    unordered_list[0], unordered_list[index_rate]
                )

            elif unordered_list[index_rate].first_currency == second_appeared_currency and index_rate != 1:
                unordered_list[index_rate], unordered_list[1] = (
                    unordered_list[1], unordered_list[index_rate]
                )

            return unordered_list
        return None

    @staticmethod
    async def execute_tasks(list_of_tasks: list) -> list:
        """Execute tasks asynchronously to get the best performance and return list of result"""

        # Run the tasks concurrently
        results = await asyncio.gather(*list_of_tasks, return_exceptions=True)

        # Add all values that are not None
        list_of_processed_tasks = [element for element in results if element is not None]

        return list_of_processed_tasks

