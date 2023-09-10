from typing import Annotated

from fastapi import Depends

from src.core.service import Service
from src.services.banks_service import BanksService

AllBanksServices = Annotated[Service, Depends(BanksService)]