from pydantic import BaseModel


class DatabaseConfig(BaseModel):
    db_host: None | str = ''
    db_port: None | str = ''
    db_database: None | str = ''
    db_user: None | str = ''
    db_password: None | str = ''
    db_type: None | str = ''
    db_driver: None | str = ''