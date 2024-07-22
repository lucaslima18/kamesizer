from PIL.PngImagePlugin import PngImageFile
from PIL.JpegImagePlugin import JpegImageFile
from src.modules.image_resize.ext import (
    ImageMaxSizeExceededError,
    ImageNegativeSizeError,
    IncorrectImageFormatError,
    ResizeToOriginalValueError,
    ImageAlreadyOnMaxSizeError,
)


class ImageValidator:
    @staticmethod
    def max_size_exceded(new_width: int, new_height: int) -> None:
        if new_width > 15360 or new_height > 8640:
            raise ImageMaxSizeExceededError(
                {
                    "message": "As dimensões digitadas excedem os padrões permitidos pelo sistema 15360X8640."
                }
            )

    @staticmethod
    def size_is_positive(new_width: int, new_height: int) -> None:
        if new_width <= 0 or new_height <= 0:
            raise ImageNegativeSizeError(
                {"message": "As dimensões digitadas devem ser positivas."}
            )

    @staticmethod
    def already_on_max_size(image: PngImageFile | JpegImageFile) -> None:
        width, height = image.size

        if width == 15360 and height == 8640:
            raise ImageAlreadyOnMaxSizeError(
                {
                    "message": "Não foi possível fazer o redimensionamento pois a imagem já está no tamanho máximo suportado."
                }
            )

    @staticmethod
    def resize_to_original_value(
        image: PngImageFile | JpegImageFile, new_width: int, new_height: int
    ) -> None:
        width, height = image.size

        if width == new_width and height == new_height:
            raise ResizeToOriginalValueError(
                {
                    "message": "O tamanho da imagem não pode ser redimensionado para o valor original."
                }
            )

    @staticmethod
    def format_is_valid(image: PngImageFile | JpegImageFile) -> None:
        if image.format not in {"PNG", "JPG", "JPEG"}:
            raise IncorrectImageFormatError(
                {
                    "message": "Formato de imagem não suportado! formatos aceitos: JPG, JPEG, PNG."
                }
            )
