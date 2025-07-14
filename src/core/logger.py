"""Logging setup."""

import logging


def get_logger(name: str) -> logging.Logger:
    """Return application logger."""
    return logging.getLogger(name)
