import asyncio
from typing import Final

from api.schemas import ExchangeRate, InternationalCurrency


class Service:
    first_appeared_currency: Final = InternationalCurrency.usd
    second_appeared_currency: Final = InternationalCurrency.eur

    @staticmethod
    async def set_two_first_appeared(
            unordered_list: list[ExchangeRate],
            first_appeared_currency: str,
            second_appeared_currency: str
    ) -> list[ExchangeRate]:

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

    @staticmethod
    async def execute_tasks(list_of_tasks: list) -> list:
        """Execute tasks asynchronously to get the best performance and return list of result"""

        # Run the tasks concurrently
        results = await asyncio.gather(*list_of_tasks, return_exceptions=True)

        # Add all values that are not None
        list_of_processed_tasks = [element for element in results if element is not None]

        return list_of_processed_tasks
