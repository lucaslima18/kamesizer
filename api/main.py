from src.shared.utils.log_handler import LogHandler
from src.libs.api.api_handler import APIHandler
from src.modules.image_resize.controller import ImageResizeController


logger: LogHandler = LogHandler()

api = APIHandler()
api.inject_router(ImageResizeController.router)
api.start()