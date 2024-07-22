from fastapi import UploadFile
from PIL import Image

from src.shared.utils.config import get_config
from src.shared.utils.log_handler import LogHandler
from .validators.image_validator import ImageValidator

logger = LogHandler()


class ImageResizeService:
    def __init__(self) -> None:
        self.config = get_config()

    def create_image(self, file: UploadFile, new_width: int, new_height: int):
        image = Image.open(file.file)
        logger.info(type(image))

        # ImageValidator.already_on_max_size(image=image)
        ImageValidator.resize_to_original_value(
            image=image, new_width=new_width, new_height=new_height
        )
        ImageValidator.size_is_positive(new_width=new_width, new_height=new_height)
        ImageValidator.max_size_exceded(new_width=new_width, new_height=new_height)
        ImageValidator.format_is_valid(image=image)
        
        

        # resized_image = image.resize((new_width, new_height))
        # resized_image.save(
        #     fp=f"{self.config.API_STORAGE_PATH}/{file.filename}",
        #     format=image.format,
        # )

        return f"{self.config.API_STORAGE_PATH}/{file.filename}"
