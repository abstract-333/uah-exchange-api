from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """There fields are rewritten by env file"""

    server_host: str = "0.0.0.0"
    server_port: int = 8000

    redis_host: str = "0.0.0.0"
    redis_port: str = "6379"
    redis_directory: str = ""
    redis_secret_key: str

    @property
    def redis_url(self):
        return f"redis://{self.redis_host}:{self.redis_port}/{self.redis_directory}"


settings = Settings(_env_file=".env", _env_file_encoding="utf-8")  # type: ignore
