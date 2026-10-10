"""Logging setup: writes to both a log file and the console."""
import logging
import os


def setup_logger(log_file, level="INFO"):
    os.makedirs(os.path.dirname(log_file), exist_ok=True)
    logger = logging.getLogger("sis")
    if logger.handlers:  # avoid duplicate handlers on repeated calls
        return logger
    logger.setLevel(getattr(logging, str(level).upper(), logging.INFO))
    fmt = logging.Formatter("%(asctime)s | %(levelname)-8s | %(message)s")

    file_handler = logging.FileHandler(log_file, encoding="utf-8")
    file_handler.setFormatter(fmt)
    logger.addHandler(file_handler)

    console = logging.StreamHandler()
    console.setLevel(logging.WARNING)  # keep the menu clean
    console.setFormatter(fmt)
    logger.addHandler(console)
    return logger
