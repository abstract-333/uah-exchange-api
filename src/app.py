from fastapi import FastAPI

from api.api import cash_router

app = FastAPI()

app.include_router(cash_router)

