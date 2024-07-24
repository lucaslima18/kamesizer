import os, uuid
from abc import ABC, abstractmethod
from PIL.PngImagePlugin import PngImageFile
from PIL.JpegImagePlugin import JpegImageFile


class StorageInterface(ABC):

    @abstractmethod
    def save_file(self, file, image: PngImageFile | JpegImageFile): ...


class LocalStorage(StorageInterface):
    def __init__(self, storage_path: str) -> None:
        self.storage_path = storage_path

    def save_file(self, file, image: PngImageFile | JpegImageFile) -> str:
        filename = uuid.uuid4().hex + "_" + file.filename
        image.save(fp=f"{self.storage_path}/{filename}", format=image.format)

        return filename
