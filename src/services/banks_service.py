from src.api.schemas import BankExchangeRate
from src.core.service import Service
from src.services.avalbank_service import AvalBankService
from src.services.centralbank_service import CentralBankService
from src.services.monobank_service import MonoBankService
from src.services.privatebank_service import PrivatBankService
from src.utils.async_tasks import execute_tasks


class BanksService(Service):
    banks_list: list[Service] = [
        AvalBankService(),
        CentralBankService(),
        MonoBankService(),
        PrivatBankService(),
    ]

    async def get_cash_exchange_rate(self) -> list[BankExchangeRate]:
        tasks = [
            bank_service.get_cash_exchange_rate() for bank_service in self.banks_list
        ]

        list_of_rates = await execute_tasks(tasks)

        return list_of_rates

    async def get_online_exchange_rate(self) -> list[BankExchangeRate]:
        tasks = [
            bank_service.get_online_exchange_rate() for bank_service in self.banks_list
        ]

        list_of_rates = await execute_tasks(tasks)

        return list_of_rates
