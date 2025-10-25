"""Utility module for configuring logging.

This module centralizes logging configuration for the API testing framework.  It
sets up both console and file handlers so that logs are recorded during test
execution.  Detailed reporting and logging are critical for understanding test
results and diagnosing issues【294264666156480†L290-L299】.
"""

import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path


def setup_logger(name: str = "api_logger",
                 log_file: str = None,
                 level: int = logging.INFO) -> logging.Logger:
    """Create and configure a logger.

    Parameters
    ----------
    name: str
        The name of the logger to create.
    log_file: str, optional
        File path where logs should be written.  If None, logs are not written
        to disk.
    level: int
        Logging level (e.g. logging.INFO, logging.DEBUG).

    Returns
    -------
    logging.Logger
        Configured logger instance.
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # Avoid adding duplicate handlers if logger already configured.
    if logger.handlers:
        return logger

    # Console handler
    console_handler = logging.StreamHandler()
    console_format = logging.Formatter(
        "%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    console_handler.setFormatter(console_format)
    logger.addHandler(console_handler)

    # File handler (rotating) if file is specified
    if log_file:
        path = Path(log_file)
        path.parent.mkdir(parents=True, exist_ok=True)
        file_handler = RotatingFileHandler(path, maxBytes=1_000_000, backupCount=3)
        file_format = logging.Formatter(
            "%(asctime)s [%(levelname)s] %(name)s: %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        file_handler.setFormatter(file_format)
        logger.addHandler(file_handler)

    return logger