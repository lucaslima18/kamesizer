import base64
from fastapi import UploadFile
from PIL import Image

from src.libs.message_broker.rabbitmq_handler import RabbitMQHandler
from src.shared.utils.config import get_config
from src.shared.utils.log_handler import LogHandler
from .validators.image_validator import ImageValidator
from .interfaces.storage_interface import StorageInterface
from .repository import ImageRepository
from .models import Images

logger = LogHandler()


class ImageResizeService:
    def __init__(self) -> None:
        self.config = get_config()
        self.repository = ImageRepository()

    def create_image(
        self,
        storage: StorageInterface,
        file: UploadFile,
        new_width: int,
        new_height: int,
    ):
        image = Image.open(file.file)

        ImageValidator.already_on_max_size(image=image)
        ImageValidator.resize_to_original_value(
            image=image, new_width=new_width, new_height=new_height
        )
        ImageValidator.size_is_positive(new_width=new_width, new_height=new_height)
        ImageValidator.max_size_exceded(new_width=new_width, new_height=new_height)
        ImageValidator.format_is_valid(image=image)

        new_filename = storage.save_file(image=image)
        image_path = storage.get_file(file_name=new_filename)

        with open(image_path, "rb") as test:
            image_encoded = base64.b64encode(test.read()).decode("utf-8")

        message = {
            "file_name": new_filename,
            "new_width": new_width,
            "new_height": new_height,
            "image_data": image_encoded,
        }

        self.repository.create_image(image=Images(image_name=new_filename))

        rabbitmq = RabbitMQHandler()
        rabbitmq.send_message(data=message)

        self.repository.update_resize_status(
            image_name=new_filename, resize_status="in-queue"
        )

        return {
            "message": "the image has been sent to resize file and will be available soon, please follow the /get_status/ endpoint!",
            "file_name": new_filename,
        }

    def get_status(self, storage: StorageInterface, file_name: str):
        image_exists = self.repository.get_by_name(image_name=file_name)

        if image_exists and storage.have_resized_version(file_name=file_name):
            self.repository.update_resize_status(
                image_name=file_name, resize_status="resized"
            )

        act_status = self.repository.get_status_by_name(image_name=file_name)

        return {
            "status": (
                act_status
                if act_status != "resized"
                else "File resized, please check /resized-image/ endpoint!"
            )
        }

    def get_resized_image(self, storage: StorageInterface, file_name: str):
        image = self.repository.get_by_name(image_name=file_name)

        if image and image.resize_status == 'resized':
            image_resized_name = f"{image.image_name.split('.')[0]}-resized.{file_name.split('.')[1]}"
            return storage.get_file(file_name=image_resized_name)

