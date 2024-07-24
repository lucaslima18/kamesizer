import os, uuid
from abc import ABC, abstractmethod
from PIL.PngImagePlugin import PngImageFile
from PIL.JpegImagePlugin import JpegImageFile
from fastapi import UploadFile


class StorageInterface(ABC):

    @abstractmethod
    def get_file(self, file_name: str) -> str: ...

    @abstractmethod
    def save_file(
        self, file: UploadFile, image: PngImageFile | JpegImageFile
    ) -> str: ...

    @abstractmethod
    def have_resized_version(self, file_name: str) -> bool: ...


class LocalStorage(StorageInterface):
    def __init__(self, storage_path: str) -> None:
        self.storage_path = storage_path

    def get_file(self, file_name: str) -> PngImageFile | JpegImageFile:
        return f"{self.storage_path}/{file_name}"

    def save_file(self, image: PngImageFile | JpegImageFile) -> str:
        filename = uuid.uuid4().hex + "." + image.format.lower()
        image.save(fp=f"{self.storage_path}/{filename}", format=image.format)

        return filename

    def have_resized_version(self, file_name) -> bool:
        file_with_resized = (
            f"{file_name.split('.')[0]}-resized.{file_name.split('.')[1]}"
        )
        file = next(
            filter(
                lambda file_list: file_with_resized in file_list,
                [files for _, _, files in os.walk(self.storage_path)][0],
            ),
            None,
        )

        if file:
            return True
