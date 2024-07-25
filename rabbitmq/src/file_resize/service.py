from io import BytesIO
import base64
from PIL import Image

from src.shared.utils.config import get_config
from src.shared.utils.log_handler import LogHandler

logger = LogHandler()
config = get_config()


class FileResizerService:
    def __init__(self) -> None:
        pass

    def resize_image(
        self, file_name: str, new_width: int, new_height: int, encoded_image: str
    ):
        try:
            image = Image.open(BytesIO(base64.b64decode(encoded_image)))
            resized_image = image.resize((new_width, new_height))
            resized_file_path = f"{config.STORAGE_PATH}/{file_name.split('.')[0]}-resized.{file_name.split('.')[1]}"
            resized_image.save(
                fp=resized_file_path,
                format=image.format,
            )

            logger.info("resized image has been saved with sucessfuly!")

        except Exception as err:
            logger.error(err)
