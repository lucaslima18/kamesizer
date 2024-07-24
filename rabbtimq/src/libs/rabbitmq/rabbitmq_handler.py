import json
import time
import pika as broker

from pika.exceptions import AMQPConnectionError

from src.shared.utils.log_handler import LogHandler
from src.shared.utils.config import get_config

logger = LogHandler()
config = get_config()


class RabbitMQHandler:
    def __init__(self, callback=None):
        self.queue = config.RABBITMQ_QUEUE
        username = config.RABBITMQ_USER
        password = config.RABBITMQ_PASS
        host = config.RABBITMQ_HOST
        port = config.RABBITMQ_PORT
        credentials = broker.PlainCredentials(username, password)

        self.callback = callback
        self.connection = ""
        self.channel = ""
        self.parameters = broker.ConnectionParameters(
            credentials=credentials,
            host=host,
            port=int(port),
            virtual_host="/",
            heartbeat=60,
        )

    def bootstrap(self):
        try:
            self.connection = broker.BlockingConnection(self.parameters)
            self.channel = self.connection.channel()
            self.channel.exchange_declare(
                exchange='resize_image',
                exchange_type='direct'
            )
            self.channel.queue_declare(queue=self.queue)
            self.channel.queue_bind(
                queue=self.queue,
                exchange='resize_image',
                routing_key='RESIZE_IMAGE'
            )

            self.channel.basic_consume(
                queue=self.queue, on_message_callback=self.callback, auto_ack=False
            )
            logger.info("RabbitMQ Connected")
            self.channel.start_consuming()
        except AMQPConnectionError as err:
            logger.error(err)
            time.sleep(5000)
