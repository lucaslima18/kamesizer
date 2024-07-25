import coloredlogs
import logging

from src.shared.utils.config import get_config

config = get_config()


class LogHandler(coloredlogs.ColoredFormatter):
    def __init__(
        self,
        format="[%(levelname)s] - %(asctime)s, [%(name)s] %(message)s",
        level=config.API_LOG_LEVEL
    ):
        self.format = format
        self.level = level
        self.logger = logging.getLogger()
        super().__init__(self.format, self.level)
        coloredlogs.install(level=self.level, fmt=self.format)

    def reset_logger(self) -> None:
        self.format = "[%(levelname)s] - %(asctime)s, [%(name)s] %(message)s"
        coloredlogs.install(level=self.level, fmt=self.format)

    def info(self, msg, extra=None) -> None:
        self.logger.info(msg, extra=extra)

    def error(self, msg, extra=None) -> None:
        self.logger.error(msg, extra=extra)

    def debug(self, msg, extra=None) -> None:
        self.logger.debug(msg, extra=extra)

    def warn(self, msg, extra=None) -> None:
        self.logger.warn(msg, extra=extra)
