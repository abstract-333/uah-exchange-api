import time
from enum import Enum
from typing import Final

from pydantic import BaseModel, Field


class InternationalCurrency(str, Enum):
    usd: Final = 'USD'
    eur: Final = 'EUR'


class NationalCurrency(str, Enum):
    uah: Final = "UAH"


class ExchangeRate(BaseModel):
    first_currency: InternationalCurrency = Field(max_length=3, min_length=3, examples=["USD", "EUR"])
    second_currency: NationalCurrency = Field(max_length=3, min_length=3, examples=["UAH"])
    date: str = Field(description="Unix time from 1970", default=str(int(time.time())))
    buy: float = Field(examples=[37.75])
    sell: float = Field(examples=[38.75])


class BankExchangeRate(BaseModel):
    bank_name: str = Field(examples=["PrivatBank", "MonoBank"])
    rates: list[ExchangeRate]
