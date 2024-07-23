import os
import json
import time
import pika as broker

from dotenv import load_dotenv, find_dotenv
from pika.exceptions import AMQPConnectionError

from src.shared.utils.logs import LogHandler

load_dotenv(find_dotenv())
logger = LogHandler()


class RabbitMQ:
    def __init__(self, callback=None):
        self.queue = "DATATCU_WEBSCRAPING_QUEUE"
        username = os.getenv("RABBITMQ_USER")
        password = os.getenv("RABBITMQ_PASS")
        host = os.getenv("RABBITMQ_HOST")
        port = os.getenv("RABBITMQ_PORT")
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

    def send_message(self, data):
        conn = broker.BlockingConnection(self.parameters)
        channel = conn.channel()
        channel.basic_publish(
            exchange="resize_image",
            routing_key="RESIZE_IMAGE",
            body=json.dumps({"data": data}),
        )
        channel.close()
        conn.close()

    def bootstrap(self):
        try:
            self.connection = broker.BlockingConnection(self.parameters)
            self.channel = self.connection.channel()
            self.channel.queue_declare(queue=self.queue)

            self.channel.basic_consume(
                queue=self.queue, on_message_callback=self.callback, auto_ack=False
            )
            logger.info("RabbitMQ Connected")
            self.channel.start_consuming()
        except AMQPConnectionError as err:
            logger.error(err)
            time.sleep(5000)
