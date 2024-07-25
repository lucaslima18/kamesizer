from typing import Dict

from sqlalchemy.future import Engine
from sqlmodel import Session, create_engine

from src.shared.utils.config import get_config
from src.shared.utils.log_handler import LogHandler
from src.libs.db.schemas import DatabaseConfig
from src.libs.db.interfaces.database_interface import Database


logger = LogHandler(
    format="[%(levelname)s] -  %(asctime)s, [database_handler.py] %(message)s"
)


class DatabaseHandler(Database):
    def __init__(
        self,
        # db_host: None | str = None,
        # db_port: None | str = None,
        # db_database: None | str = None,
        # db_user: None | str = None,
        # db_password: None | str = None,
        # db_type: None | str = None,
        # db_driver: None | str = None,
    ) -> None:
        connection_string = self.__create_connection_string__(locals())
        self.engine = create_engine(connection_string)
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
        arguments_are_empty = all(map(lambda data: data is None, args.values()))

        if arguments_are_empty:
            config_as_dict = get_config().__dict__
            config = {key.lower(): val for key, val in config_as_dict.items()}

        else:
            config = args

        config = DatabaseConfig(**config)

        if config.db_type == "sqlite":
            con_string = "sqlite:///database.sqlite"
            return con_string

        db_host = f"{config.db_host}:{config.db_port}"
        db_auth = f"{config.db_user}:{config.db_password}"
        db_database = f"{config.db_database}"
        con_string = f"{config.db_type}://{db_auth}@{db_host}/{db_database}"

        return con_string
