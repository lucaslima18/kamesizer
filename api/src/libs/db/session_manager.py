from src.libs.db.database_handler import DatabaseHandler
from src.shared.utils.config import get_config

config = get_config()
db = DatabaseHandler()


def instance_session() -> DatabaseHandler:
    return DatabaseHandler()
