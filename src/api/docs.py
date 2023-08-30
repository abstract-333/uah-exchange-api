from pydantic import BaseModel
from starlette import status

from api.schemas import ExchangeRate


class HTTPException429(BaseModel):
    detail: str

    class Config:
        json_schema_extra = {
            "example": {"detail": "Too many requests"},
        }


class HTTPException500(BaseModel):
    detail: str

    class Config:
        json_schema_extra = {
            "example": {"detail": "Will return where error happened"},
        }


get_exchange_rate_doc = {
    status.HTTP_200_OK: {
        "model": list[dict[str, list[ExchangeRate]]]
    },
    status.HTTP_429_TOO_MANY_REQUESTS: {
        "model": HTTPException429,
        "description": "Too many requests",
    },
    status.HTTP_500_INTERNAL_SERVER_ERROR: {
        "model": HTTPException500,
        "description": "Internal Server Error"
    }
}
