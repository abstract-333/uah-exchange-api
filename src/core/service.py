from abc import abstractmethod
from src.api.schemas import InternationalCurrency, ExchangeRate


class Service:
    first_appeared_currency: InternationalCurrency
    second_appeared_currency: InternationalCurrency

    @abstractmethod
    async def get_online_exchange_rate(self):
        ...

    @abstractmethod
    async def get_cash_exchange_rate(self):
        ...


async def set_first_appeared_currencies(
    unordered_list: list[ExchangeRate],
    first_appeared_currency: str,
    second_appeared_currency: str,
) -> list[ExchangeRate] | None:
    for index_rate in range(len(unordered_list) - 1):
        if (
            unordered_list[index_rate].first_currency == first_appeared_currency
            and index_rate != 0
        ):
            unordered_list[index_rate], unordered_list[0] = (
                unordered_list[0],
                unordered_list[index_rate],
            )

        elif (
            unordered_list[index_rate].first_currency == second_appeared_currency
            and index_rate != 1
        ):
            unordered_list[index_rate], unordered_list[1] = (
                unordered_list[1],
                unordered_list[index_rate],
            )

        return unordered_list
    return None
