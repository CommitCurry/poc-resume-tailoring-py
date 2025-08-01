"""Logging configuration for CommitCurry application."""

import logging
import logging.config
from datetime import datetime
from pathlib import Path


def setup_logging() -> None:
    """Configure logging to redirect all logs to timestamped files."""
    # Create logs directory if it doesn't exist
    logs_dir = Path("logs")
    logs_dir.mkdir(exist_ok=True)

    # Generate timestamp for this application run
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_filename = logs_dir / f"commitcurry_{timestamp}.log"

    # Configure logging
    logging_config = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "detailed": {
                "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                "datefmt": "%Y-%m-%d %H:%M:%S",
            },
        },
        "handlers": {
            "file": {
                "class": "logging.FileHandler",
                "filename": str(log_filename),
                "mode": "w",
                "formatter": "detailed",
                "level": "DEBUG",
            },
        },
        "root": {
            "level": "WARNING",
            "handlers": ["file"],
        },
        "loggers": {
            # Redirect griptape logs to file
            "griptape": {
                "level": "INFO",
                "handlers": ["file"],
                "propagate": False,
            },
            # Redirect google library logs to file
            "google": {
                "level": "INFO",
                "handlers": ["file"],
                "propagate": False,
            },
            # Redirect urllib3 logs (often used by HTTP libraries)
            "urllib3": {
                "level": "WARNING",
                "handlers": ["file"],
                "propagate": False,
            },
            # Redirect requests logs
            "requests": {
                "level": "WARNING",
                "handlers": ["file"],
                "propagate": False,
            },
        },
    }

    logging.config.dictConfig(logging_config)
