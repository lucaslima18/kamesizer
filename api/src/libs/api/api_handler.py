from typing import Callable

from fastapi import APIRouter, FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from src.shared.utils.config import get_config
from src.shared.utils.log_handler import LogHandler


logger: LogHandler = LogHandler()


class APIHandler:
    def __init__(self, router_prefix: str = None, port: int = None) -> None:
        config = get_config()
        self.port = int(config.API_PORT)
        if port:
            self.port = port
        self.host = config.API_HOST
        doc_urls = {}
        self.app = FastAPI(**doc_urls, title=config.API_TITLE)
        self.router = APIRouter()

        if router_prefix:
            self.router.router.prefix = router_prefix

    def inject_router(self, router: APIRouter) -> None:
        self.router.include_router(router)

    def inject_middleware(self, function: Callable):
        if hasattr(function, 'bootstrap'):
            function.bootstrap()
        self.app.middleware('http')(function())

    def reset_routers(self):
        for route in self.router.routes:
            logger.info(route)
            self.router.routes.remove(route)

    def start(self):
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=['*'],
            allow_credentials=True,
            allow_methods=['*'],
            allow_headers=['*'],
        )

        self.app.include_router(self.router)
        uvicorn_config = uvicorn.Config(
            self.app,
            host=self.host,
            port=self.port,
            log_level='info',
            reload=True
        )

        server = uvicorn.Server(config=uvicorn_config)
        server.run()
