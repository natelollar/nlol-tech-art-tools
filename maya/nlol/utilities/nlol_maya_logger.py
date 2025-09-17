import logging
import tomllib
from logging.handlers import RotatingFileHandler
from pathlib import Path

import nlol


class NlolMayaLogger:
    """Custom logging class for Maya. Writes to both console and log file."""

    def __init__(self) -> None:
        """Initialize logger with console and file handlers."""
        self.utilities_folderpath = Path(nlol.__file__).parent / "utilities"
        self.log_filepath = self.utilities_folderpath / "nlol_maya.log"

        self.logger = logging.getLogger("nlol_maya")

        if not self.logger.handlers:
            file_formatter = logging.Formatter(
                "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            )
            file_handler = RotatingFileHandler(
                self.log_filepath,
                maxBytes=5 * 1024 * 1024,
                backupCount=3,
            )
            file_handler.setFormatter(file_formatter)
            self.logger.addHandler(file_handler)

            self.get_debug_mode()
            self.set_log_level()

    def get_debug_mode(self):
        """Get debug_mode variable from "debug_toggle.toml"."""
        config_file = self.utilities_folderpath / "debug_toggle.toml"
        with open(config_file, "rb") as f:
            self.debug_mode = tomllib.load(f)["debug_mode"]

    def set_log_level(self):
        """Set the logging level based on the debug_mode variable in "debug_toggle.toml"
        Maya must be restarted when debug mode is changed.
        """
        if self.debug_mode:
            self.logger.setLevel(logging.DEBUG)
        else:
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
