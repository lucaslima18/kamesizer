import json
import pika as broker

from src.shared.utils.log_handler import LogHandler
from src.shared.utils.config import get_config

logger = LogHandler()
config = get_config()


class RabbitMQHandler:
    def __init__(self):
        self.queue = config.RABBITMQ_QUEUE
        username = config.RABBITMQ_USER
        password = config.RABBITMQ_PASS
        host = config.RABBITMQ_HOST
        port = config.RABBITMQ_PORT
        credentials = broker.PlainCredentials(username, password)
        self.parameters = broker.ConnectionParameters(
            credentials=credentials,
            host=host,
            port=int(port),
            virtual_host="/",
            heartbeat=60,
        )

    def send_message(self, data):
        conn = broker.BlockingConnection(self.parameters)
        channel = conn.channel()
        channel.basic_publish(
            exchange="resize_image",
            routing_key="RESIZE_IMAGE",
            body=json.dumps(data),
        )
        channel.close()
        conn.close()
