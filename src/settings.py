from pydantic.v1 import BaseSettings


class Settings(BaseSettings):
    """There fields are rewritten by env file"""
    server_host: str = '0.0.0.0'
    server_port: int = 8000


settings = Settings(
    _env_file='.env',
    _env_file_encoding='utf-8'
)
