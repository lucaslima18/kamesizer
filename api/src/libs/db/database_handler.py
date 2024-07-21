import os
from typing import Dict

from pydantic import BaseModel
from sqlalchemy.future import Engine
from sqlalchemy.pool import NullPool
from sqlmodel import Session, create_engine

from src.shared.utils.config import get_config
from src.shared.interfaces.database_interface import Database


class DatabaseConfig(BaseModel):
    db_host: None | str = ""
    db_port: None | str = ""
    db_database: None | str = ""
    db_user: None | str = ""
    db_password: None | str = ""
    db_type: None | str = ""
    db_driver: None | str = ""


class DatabaseHandler(Database):
    def __init__(
        self,
        db_host: None | str = None,
        db_port: None | str = None,
        db_database: None | str = None,
        db_user: None | str = None,
        db_password: None | str = None,
        db_type: None | str = None,
        db_driver: None | str = None,
    ) -> None:
        connection_string = self.__create_connection_string__(locals())
        self.engine = create_engine(
            connection_string, poolclass=NullPool, pool_recycle=0
        )
        self.session = None

    def get_engine(self) -> Engine:
        return self.engine

    def get_session(self) -> Session:
        self.session = Session(self.engine)
        return self.session

    def __enter__(self) -> Session:
        self.session = Session(self.engine, expire_on_commit=False)
        return self.session

    def __exit__(self, *args, **kwargs) -> None:
        self.session.close()

    def __create_connection_string__(self, args: Dict[str, str]) -> str:
        del args["self"]
        arguments_are_empty: bool = all(map(lambda data: data is None, args.values()))

        test_mode: bool | None = os.path.isfile("__caravel__test__running__")
        if arguments_are_empty or test_mode:
            config_as_dict: dict = get_config().__dict__
            config: dict = {key.lower(): val for key, val in config_as_dict.items()}
        else:
            config: dict = args

        config: dict = DatabaseConfig(**config)

        if config.db_type == "sqlite":
            con_string: str = "sqlite:///database.sqlite"
            return con_string
        if test_mode:
            test_db: str | None = get_config().API_TEST_DB
            config.db_database = test_db

        db_host: str = f"{config.db_host}:{config.db_port}"
        db_auth: str = f"{config.db_user}:{config.db_password}"
        db_database: str | None = config.db_database

        if config.db_driver:
            db_database: str = config.db_database + f"?driver={config.db_driver}"

        if config.db_type and config.db_type.lower() == "oracle+cx_oracle+service_name":

            con_string: str = (
                f"oracle+cx_oracle://{db_auth}@{db_host}/?service_name={config.db_database}"
            )
            return con_string

        con_string: str = f"{config.db_type}://{db_auth}@{db_host}/{db_database}"

        return con_string
