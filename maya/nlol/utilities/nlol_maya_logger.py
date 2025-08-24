import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

import nlol


class NlolMayaLogger:
    """Custom logging class for Maya. Writes to both console and log file."""

    def __init__(self) -> None:
        """Initialize logger with console and file handlers."""
        log_folderpath = Path(nlol.__file__).parent
        self.log_filepath = log_folderpath / "utilities" / "nlol_maya.log"

        self.logger = logging.getLogger("nlol_maya")

        if not self.logger.handlers:
            file_formatter = logging.Formatter(
                "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
            )
            file_handler = RotatingFileHandler(
                self.log_filepath,
                maxBytes=5 * 1024 * 1024,
                backupCount=3,
            )
            file_handler.setFormatter(file_formatter)
            self.logger.addHandler(file_handler)

            self.logger.setLevel(logging.INFO)


_logger_instance = None


def get_logger() -> logging.Logger:
    """Returns:
    Logger instance.
    """
    global _logger_instance
    if _logger_instance is None:
        maya_logger = NlolMayaLogger()
        _logger_instance = maya_logger.logger
    return _logger_instance
