"""
Production logging configuration for RepoMind AI Enterprise.

Provides centralized application logging with:
- Console output
- Rotating file logs
- Consistent formatting
"""

import logging
import sys
from logging.handlers import RotatingFileHandler
from pathlib import Path

from src.core.config import settings
from src.core.constants import LOG_FILE_NAME, LOG_FORMAT


class LoggerManager:
    """
    Manages application-wide logging configuration.
    """

    _configured = False

    @classmethod
    def configure(cls) -> None:
        """
        Configure root logger.
        """

        if cls._configured:
            return

        settings.logs_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

        log_file = Path(settings.logs_dir) / LOG_FILE_NAME

        formatter = logging.Formatter(LOG_FORMAT)

        root_logger = logging.getLogger()

        root_logger.setLevel(logging.INFO)

        root_logger.handlers.clear()

        console_handler = logging.StreamHandler(sys.stdout)

        console_handler.setFormatter(formatter)

        file_handler = RotatingFileHandler(
            filename=log_file,
            maxBytes=5 * 1024 * 1024,
            backupCount=5,
            encoding="utf-8",
        )

        file_handler.setFormatter(formatter)

        root_logger.addHandler(console_handler)

        root_logger.addHandler(file_handler)

        cls._configured = True


def get_logger(name: str) -> logging.Logger:
    """
    Get configured logger instance.

    Args:
        name:
            Logger name.

    Returns:
        logging.Logger instance.
    """

    LoggerManager.configure()

    return logging.getLogger(name)


# Application logger
logger = get_logger("RepoMindAI")
