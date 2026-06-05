import logging
import sys


def setup_logger() -> logging.Logger:
    logger = logging.getLogger("group_manager")

    logger.setLevel(logging.INFO)

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
    )

    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setFormatter(formatter)

    logger.handlers.clear()
    logger.addHandler(stream_handler)

    return logger


logger = setup_logger()