from api.schemas import ExchangeRate


class Service:

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
