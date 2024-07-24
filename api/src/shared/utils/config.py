import os
from typing import Optional
from urllib.parse import quote_plus

from dotenv import find_dotenv, load_dotenv
from pydantic import BaseModel

from src.shared.validators.boolean_env_validator import boolean_env_validator
from src.shared.validators.check_log_level import check_log_level

load_dotenv(find_dotenv())


class GeneralConfig(BaseModel):
    API_TITLE: str = os.getenv("API_TITLE")
    API_PRD: Optional[bool] = boolean_env_validator(os.getenv("API_PRD"))
    API_PORT: Optional[int] = os.getenv("API_PORT", default=8000)
    API_HOST: str = os.getenv("API_HOST")
    API_LOG_LEVEL: str = check_log_level(
        act_log_level=os.getenv("API_LOG_LEVEL", default="info")
    )
    API_STORAGE_PATH: str = os.getenv("API_STORAGE_PATH", default="../storage/")
    DB_TYPE: str = os.getenv("DB_TYPE")
    DB_HOST: str = os.getenv("DB_HOST")
    DB_DATABASE: str = os.getenv("DB_DATABASE")
    DB_PORT: str = os.getenv("DB_PORT")
    DB_USER: str = os.getenv("DB_USER")
    DB_PASSWORD: str = quote_plus(os.getenv("DB_PASSWORD", ""))
    DB_DRIVER: Optional[str] = os.getenv("DB_DRIVER")
    RABBITMQ_USER: str = os.getenv("RABBITMQ_USER")
    RABBITMQ_PASS: str = os.getenv("RABBITMQ_PASS")
    RABBITMQ_HOST: str = os.getenv("RABBITMQ_HOST")
    RABBITMQ_PORT: str = os.getenv("RABBITMQ_PORT")
    RABBITMQ_QUEUE: str = os.getenv("RABBITMQ_QUEUE")


def get_config() -> GeneralConfig:
    return GeneralConfig()
