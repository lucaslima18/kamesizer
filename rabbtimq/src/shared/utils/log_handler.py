import coloredlogs
import logging


class LogHandler(coloredlogs.ColoredFormatter):
    def __init__(
        self,
        format="[%(levelname)s] - %(asctime)s, [%(name)s] %(message)s",
        level='info'
    ):
        self.format = format
        self.level = level
        self.logger = logging.getLogger()
        super().__init__(self.format, self.level)
        coloredlogs.install(level=self.level, fmt=self.format)

    def reset_logger(self):
        self.format = "[%(levelname)s] - %(asctime)s, [%(name)s] %(message)s"
        coloredlogs.install(level=self.level, fmt=self.format)

    def info(self, msg, extra=None):
        self.logger.info(msg, extra=extra)

    def error(self, msg, extra=None):
        self.logger.error(msg, extra=extra)

    def debug(self, msg, extra=None):
        self.logger.debug(msg, extra=extra)

    def warn(self, msg, extra=None):
        self.logger.warn(msg, extra=extra)
