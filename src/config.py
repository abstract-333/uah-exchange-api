import os
from dotenv import load_dotenv

load_dotenv()

REDIS_HOST = os.environ.get("REDIS_HOST")
REDIS_PORT = os.environ.get("REDIS_PORT")
REDIS_URL = os.environ.get("REDIS_URL")

REDIS_SECRET_KEY = os.environ.get("REDIS_SECRET_KEY")

MODE = os.environ.get("MODE")
