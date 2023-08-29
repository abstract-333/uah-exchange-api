from enum import Enum

from pydantic import BaseModel, Field


class CurrencySecond(str, Enum):
    uah = "UAH"


class CurrencyFirst(str, Enum):
    usd = 'USD'
    eur = 'EUR'


class ExchangeRate(BaseModel):
    first_currency: CurrencyFirst = Field(max_length=3, min_length=2, examples=["USD", "EUR"])
    second_currency: CurrencySecond = Field(max_length=3, min_length=2, examples=["UAH"])
    date: str = Field(description="Unix time from 1970")
    rate_buy_first: float = Field(examples=[37.75])
    rate_sell_first: float = Field(examples=[38.75])
