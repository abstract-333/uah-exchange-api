from pydantic import BaseModel
from starlette import status

from api.schemas import ExchangeRate


class HTTPException429(BaseModel):
    detail: str

    class Config:
        json_schema_extra = {
            "example": {"detail": "Too many requests"},
        }


get_cash_exchange_rate_doc = {
    status.HTTP_200_OK: {
        "model": ExchangeRate
    },
    status.HTTP_429_TOO_MANY_REQUESTS: {
        "model": HTTPException429,
        "description": "Too many requests",
    },
}
