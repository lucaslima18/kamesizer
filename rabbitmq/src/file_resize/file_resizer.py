from io import BytesIO
import base64
from PIL import Image
from src.shared.utils.config import get_config

config = get_config()


class FileResizer:
    def __init__(self) -> None:
        pass

    def resize_image(self, file_name: str, new_width: int, new_height: int, encoded_image: str):
        image = Image.open(BytesIO(base64.b64decode(encoded_image)))
        resized_image = image.resize((new_width, new_height))
        resized_image.save(
            fp=f"{config.STORAGE_PATH}/{file_name.split('.')[0]}-resized.{file_name.split('.')[1]}",
            format=image.format,
        )
