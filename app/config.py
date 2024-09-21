import logging
from typing import Literal

from pydantic_settings import BaseSettings


class AppConfig(BaseSettings):
    log_level: Literal[10, 20, 30, 40, 50] = logging.DEBUG
    secret_key: str = "your_secret_key"
    algorithm: str = "HS256"
    acess_token_expire_minutes: int = 30
    root_username: str = "root"
    root_password: str = "root"

    class Config:
        case_sensitive = False
        env_file_encoding = "utf-8"
        env_nested_delimiter = "__"
        env_prefix = "GUARD_"


app_config = AppConfig()
