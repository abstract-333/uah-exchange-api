import time
from enum import Enum
from typing import Final

from pydantic import BaseModel, Field, ConfigDict


class BanksAvailable(str, Enum):
    aval_bank = "AvalBank"
    central_bank = "CentralBank"
    mono_bank = "MonoBank"
    oschad_bank = "OschadBank"
    privat_bank = "PrivatBank"
    pumb_bank = "PumbBank"
    universal_bank = "UniversalBank"


class InternationalCurrency(str, Enum):
    usd: Final = "USD"
    eur: Final = "EUR"


class NationalCurrency(str, Enum):
    uah: Final = "UAH"


class ExchangeRate(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    first_currency: InternationalCurrency = Field(
        max_length=3, min_length=3, examples=["USD", "EUR"]
    )
    second_currency: NationalCurrency = Field(
        max_length=3, min_length=3, examples=["UAH"]
    )
    date: str = Field(description="Unix time from 1970", default=str(int(time.time())))
    buy: float = Field(ge=0, examples=[37.75])
    sell: float = Field(ge=0, examples=[38.75])


class BankExchangeRate(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    bank_name: str = Field(examples=["PrivatBank", "MonoBank"])
    rates: list[ExchangeRate] | None
