import logging
import sys
from logging.handlers import RotatingFileHandler


def setup_logging(level=logging.INFO):

    log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

    console_handler = logging.StreamHandler(sys.stdout)

    file_handler = RotatingFileHandler(
        "app_events.log", maxBytes=5_000_000, backupCount=3, encoding="utf-8"
    )

    # Configure the root logger to output to the console
    logging.basicConfig(
        level=level, format=log_format, handlers=[console_handler, file_handler]
    )
