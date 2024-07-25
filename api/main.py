from src.shared.utils.log_handler import LogHandler
from src.libs.api.api_handler import APIHandler
from src.modules.image_resize.controller import ImageResizeController
from src.shared.utils.load_icon import load_icon

logger: LogHandler = LogHandler()

load_icon()

api = APIHandler()
api.inject_router(ImageResizeController.router)
api.start()
