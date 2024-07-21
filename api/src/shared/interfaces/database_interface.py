from abc import ABC, abstractmethod

from sqlmodel import Session


class Database(ABC):

    @abstractmethod
    def get_session(self):
        pass

    @abstractmethod
    def __init__(self) -> Session:
        pass

    @abstractmethod
    def __exit__(self, *args, **kwargs) -> None:
        pass
