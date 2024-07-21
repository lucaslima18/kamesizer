from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from PIL import UnidentifiedImageError
from fastapi import UploadFile

from src.shared.utils.config import get_config
from src.shared.utils.log_handler import LogHandler
from .ext import IncorrectImageFormat
from .service import ImageResizeService

config = get_config()
logger = LogHandler()


class ImageResizeController:

    prefix = "image-resizer"
    router = APIRouter(prefix=f"/{prefix}")

    @router.post("")
    def create_image(file: UploadFile, new_width: int, new_height: int):
        try:
            file_path = ImageResizeService().create_image(
                file=file, new_width=new_width, new_height=new_height
            )
            return FileResponse(path=file_path)

        except UnidentifiedImageError:
            raise HTTPException(
                status_code=400,
                detail={
                    "message": "Formato incorreto de imagem! verifique o arquivo e tente novamente."
                },
            )

        except IncorrectImageFormat as err:
            raise HTTPException(status_code=400, detail=err.args[0])
