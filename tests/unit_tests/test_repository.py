import pytest
from src.core.repository import Repository
from src.core.urls import (
    CENTRAL_BANK_ONLINE_URL,
    PRIVAT_BANK_ONLINE_URL,
    PRIVAT_BANK_CASH_URL,
    MONO_BANK_ONLINE_URL,
    AVAL_BANK_CASH_URL,
    UNIVERSAL_BANK_URL,
    PUMB_BANK_URL
)


class TestRepository:
    @pytest.mark.parametrize(
        "url, status_code",
        [
            (CENTRAL_BANK_ONLINE_URL, 200),
            (MONO_BANK_ONLINE_URL, 200),
            (PRIVAT_BANK_CASH_URL, 200),
            (PRIVAT_BANK_ONLINE_URL, 200),
            (UNIVERSAL_BANK_URL, 200),
            (AVAL_BANK_CASH_URL + "USD", 200),
            (AVAL_BANK_CASH_URL + "EUR", 200),
            (PUMB_BANK_URL, 200),
            ("NOT_URL", 503),
        ]
    )
    @pytest.mark.anyio
    async def test_get_request_success(self, url, status_code):
        assert (await Repository.get_request(url))[0] == status_code

