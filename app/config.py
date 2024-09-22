import logging
from typing import Literal

from pydantic_settings import BaseSettings


class AppConfig(BaseSettings):
    log_level: Literal[10, 20, 30, 40, 50] = logging.DEBUG
    secret_key: str = "your_secret_key"
    algorithm: str = "HS256"
    access_token_lifetime_minutes: int = 60
    session_lifetime_days: int = 30

    class Config:
        case_sensitive = False
        env_file_encoding = "utf-8"
        env_nested_delimiter = "__"
        env_prefix = "GUARD_"


app_config = AppConfig()
