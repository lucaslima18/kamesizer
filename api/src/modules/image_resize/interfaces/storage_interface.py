import os, uuid
from abc import ABC, abstractmethod
from PIL.PngImagePlugin import PngImageFile
from PIL.JpegImagePlugin import JpegImageFile
from fastapi import UploadFile


class StorageInterface(ABC):

    @abstractmethod
    def get_file(self, file_name: str): ...

    @abstractmethod
    def save_file(self, file: UploadFile, image: PngImageFile | JpegImageFile): ...


class LocalStorage(StorageInterface):
    def __init__(self, storage_path: str) -> None:
        self.storage_path = storage_path

    def get_file(self, file_name: str) -> PngImageFile | JpegImageFile:
        file = next(
            filter(
                lambda file_list: file_name in file_list,
                [files for _, _, files in os.walk(self.storage_path)][0],
            ),
            None
        )

        if not file:
            ...

        return f"{self.storage_path}/{file}"

    def save_file(self, file: UploadFile, image: PngImageFile | JpegImageFile) -> str:
        filename = uuid.uuid4().hex + "_" + file.filename
        image.save(fp=f"{self.storage_path}/{filename}", format=image.format)

        return filename
