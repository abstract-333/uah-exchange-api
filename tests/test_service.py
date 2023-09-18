from typing import Any

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


@pytest.mark.anyio
class TestRepository:

    @pytest.mark.parametrize(
        "url, status_code",
        [
            (CENTRAL_BANK_ONLINE_URL, 200),
            (MONO_BANK_ONLINE_URL, 200),
            (PRIVAT_BANK_CASH_URL, 200),
            (PRIVAT_BANK_ONLINE_URL, 200),
            (UNIVERSAL_BANK_URL, 200),
        ]
    )
    async def test_get_request_json(self, url, status_code):
        assert (await Repository.get_request(url))[0] == status_code

    @pytest.mark.parametrize(
        "url, status_code",
        [
            (AVAL_BANK_CASH_URL, 200),
            (PUMB_BANK_URL, 200),
        ]
    )
    async def test_get_request_text(self, url, status_code):
        assert (await Repository.get_request(url))[0] == status_code
