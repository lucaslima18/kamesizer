from io import BytesIO
from fastapi import UploadFile
from PIL import Image

from src.shared.utils.config import get_config
from src.shared.utils.log_handler import LogHandler
from .ext import IncorrectImageFormat

logger = LogHandler()


class ImageResizeService:
    def __init__(self) -> None:
        self.config = get_config()

    def create_image(self, file: UploadFile, new_width: int, new_height: int):
        image = Image.open(file.file)
        if image.format not in {"PNG", "JPG", "JPEG"}:
            raise IncorrectImageFormat(
                {
                    "message": "Formato de imagem não suportado! formatos aceitos: JPG, JPEG, PNG."
                }
            )

        resized_image = image.resize((new_width, new_height))
        resized_image.save(
            fp=f"{self.config.API_STORAGE_PATH}/{file.filename}",
            format=image.format,
        )

        # return {
        #     "filename": file.filename,
        #     "message": f"start resize of image to {new_width}X{new_height}",
        #     "test": image.format,
        # }
        return f"{self.config.API_STORAGE_PATH}/{file.filename}"
