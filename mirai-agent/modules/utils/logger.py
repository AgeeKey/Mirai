"""
Единая система логирования для всего проекта.
"""

import logging
import sys
from pathlib import Path
from logging.handlers import RotatingFileHandler


class Logger:
    """Универсальный логгер с кешированием экземпляров."""

    _loggers: dict[str, logging.Logger] = {}

    def __init__(self, name: str, log_dir: str = "data/logs"):
        self.name = name
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(parents=True, exist_ok=True)

        if name in Logger._loggers:
            self.logger = Logger._loggers[name]
        else:
            self.logger = self._create_logger()
            Logger._loggers[name] = self.logger

    def _create_logger(self) -> logging.Logger:
        logger = logging.getLogger(self.name)
        logger.setLevel(logging.DEBUG)
        logger.handlers.clear()

        formatter = logging.Formatter(
            "[%(asctime)s] [%(name)s] [%(levelname)s] %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )

        console = logging.StreamHandler(sys.stdout)
        console.setLevel(logging.INFO)
        console.setFormatter(formatter)
        logger.addHandler(console)

        log_file = self.log_dir / f"{self.name.lower()}.log"
        file_handler = RotatingFileHandler(
            log_file,
            maxBytes=10 * 1024 * 1024,
            backupCount=5,
            encoding="utf-8",
        )
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

        error_file = self.log_dir / f"{self.name.lower()}_error.log"
        error_handler = RotatingFileHandler(
            error_file,
            maxBytes=10 * 1024 * 1024,
            backupCount=5,
            encoding="utf-8",
        )
        error_handler.setLevel(logging.ERROR)
        error_handler.setFormatter(formatter)
        logger.addHandler(error_handler)

        return logger

    def debug(self, msg, *args, **kwargs):  # noqa: D401
        self.logger.debug(msg, *args, **kwargs)

    def info(self, msg, *args, **kwargs):  # noqa: D401
        self.logger.info(msg, *args, **kwargs)

    def warning(self, msg, *args, **kwargs):  # noqa: D401
        self.logger.warning(msg, *args, **kwargs)

    def error(self, msg, *args, **kwargs):  # noqa: D401
        self.logger.error(msg, *args, **kwargs)

    def critical(self, msg, *args, **kwargs):  # noqa: D401
        self.logger.critical(msg, *args, **kwargs)
