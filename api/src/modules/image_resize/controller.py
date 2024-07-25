from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from PIL import UnidentifiedImageError
from fastapi import UploadFile

from src.shared.utils.config import get_config
from src.shared.utils.log_handler import LogHandler
from .ext import (
    ImageMaxSizeExceededError,
    ImageNegativeSizeError,
    IncorrectImageFormatError,
    ResizeToOriginalValueError,
    ImageAlreadyOnMaxSizeError,
    ImageNotFound,
    StillNotResized
)
from .service import ImageResizeService
from .interfaces.storage_interface import LocalStorage

config = get_config()
logger = LogHandler()


class ImageResizeController:

    prefix = "image-resizer"
    router = APIRouter(prefix=f"/{prefix}")

    @router.post("/resize")
    def create_image(file: UploadFile, new_width: int, new_height: int):
        try:
            return ImageResizeService().create_image(
                storage=LocalStorage(storage_path=config.API_STORAGE_PATH),
                file=file,
                new_width=new_width,
                new_height=new_height,
            )

        except UnidentifiedImageError:
            raise HTTPException(
                status_code=400,
                detail={
                    "message": "Formato de imagem não suportado! formatos aceitos: JPG, JPEG, PNG."
                },
            )

        except (
            ImageMaxSizeExceededError,
            ImageNegativeSizeError,
            IncorrectImageFormatError,
            ResizeToOriginalValueError,
            ImageAlreadyOnMaxSizeError,
        ) as err:
            raise HTTPException(status_code=400, detail=err.args[0])

    @router.get("/resize-status")
    def search_image_by_status(file_name: str):
        try:
            return ImageResizeService().get_status(
                storage=LocalStorage(storage_path=config.API_STORAGE_PATH),
                file_name=file_name,
            )

        except ImageNotFound as err:
            raise HTTPException(status_code=404, detail=err.args[0])

    @router.post("/resized-image")
    def resized_image(file_name: str):
        try:
            image_path = ImageResizeService().get_resized_image(
                storage=LocalStorage(storage_path=config.API_STORAGE_PATH),
                file_name=file_name,
            )

            return FileResponse(path=image_path)
        except StillNotResized as err:
            raise HTTPException(status_code=400, detail=err.args[0])
