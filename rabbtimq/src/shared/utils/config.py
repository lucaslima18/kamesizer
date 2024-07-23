import os

from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())


class GeneralConfig:
    RABBITMQ_PORT = os.getenv('RABBITMQ_PORT')
    RABBITMQ_HOST = os.getenv('RABBITMQ_HOST')
    RABBITMQ_USER = os.getenv('RABBITMQ_USER')
    RABBITMQ_PASS = os.getenv('RABBITMQ_PASS')
    RABBITMQ_QUEUE = os.getenv('RABBITMQ_QUEUE')


def get_config() -> GeneralConfig:
    return GeneralConfig()
