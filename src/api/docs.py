from pydantic import BaseModel

from src.api.schemas import ExchangeRate


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


get_exchange_rate_all_banks_doc = {
    200: {
        "model": list[dict[str, list[ExchangeRate]]]
    },
    429: {
        "model": HTTPException429,
        "description": "Too many requests",
    },
    500: {
        "model": HTTPException500,
        "description": "Internal Server Error"
    }
}


get_exchange_rate_bank_doc = {
    200: {
        "model": dict[str, list[ExchangeRate]]
    },
    429: {
        "model": HTTPException429,
        "description": "Too many requests",
    },
    500: {
        "model": HTTPException500,
        "description": "Internal Server Error"
    }
}
