import json
import time

from src.libs.rabbitmq.rabbitmq_handler import RabbitMQHandler
from src.shared.utils.log_handler import LogHandler
from src.shared.utils.config import get_config
from src.file_resize.file_resizer import FileResizer

logger = LogHandler()
config = get_config()


class Application:
    def __init__(self) -> None:
        logger.info("RabbitMQ Starting...")
        self.rabbitmq = RabbitMQHandler(self.callback)
        self.rabbitmq.bootstrap()

    def callback(self, ch, method, _props, body):
        try:
            data = json.loads(body)

            ch.basic_ack(delivery_tag=method.delivery_tag)
            ch.close()

            fr = FileResizer()
            fr.resize_image(
                file_name=data["file_name"],
                new_width=data["new_width"],
                new_height=data["new_height"],
                encoded_image=data["image_data"],
            )

        except Exception as err:
            logger.error(err)


if __name__ == "__main__":
    try:
        while True:
            Application()

    except KeyboardInterrupt:
        ...
