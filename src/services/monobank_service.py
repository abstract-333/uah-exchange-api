from starlette.responses import JSONResponse

from core.repository import Repository
from core.urls import MONO_BANK_ONLINE


class MonoBankService:
    url_online = MONO_BANK_ONLINE
    repo = Repository()

    async def get_online_exchange_rate(self):
        """Get online exchange rate in monobank"""
        status_code, response = await self.repo.get_request(url=self.url_online)
        if status_code != 200:
            return JSONResponse(status_code=status_code, content=response)


