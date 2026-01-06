"""Centralized logging configuration for Jackfield Labeler."""

import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path


def get_logger(name: str) -> logging.Logger:
    """
    Get a logger instance for a module.

    Args:
        name: Module name (typically __name__)

    Returns:
        Configured logger instance
    """
    # Ensure consistent naming
    if not name.startswith("jackfield_labeler"):
        name = f"jackfield_labeler.{name.split('.')[-1]}"

    return logging.getLogger(name)


def configure_logging(level: str = "INFO", log_to_file: bool = False, log_file_path: str | None = None) -> None:
    """
    Configure the application-wide logging system.

    Args:
        level: Log level (DEBUG, INFO, WARNING, ERROR)
        log_to_file: Whether to log to a file
        log_file_path: Path to log file (if log_to_file is True)
    """
    # Get root logger for jackfield_labeler
    logger = logging.getLogger("jackfield_labeler")
    logger.setLevel(getattr(logging, level.upper(), logging.INFO))

    # Clear existing handlers
    logger.handlers.clear()

    # Define format
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # Console handler (always enabled)
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # File handler (conditional)
    if log_to_file and log_file_path:
        try:
            # Ensure parent directory exists
            log_path = Path(log_file_path)
            log_path.parent.mkdir(parents=True, exist_ok=True)

            # Rotating file handler (10MB, 3 backups)
            file_handler = RotatingFileHandler(
                log_file_path,
                maxBytes=10 * 1024 * 1024,
                backupCount=3,
                encoding="utf-8",  # 10 MB
            )
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)

            logger.info(f"File logging enabled: {log_file_path}")

        except Exception:
            logger.exception("Failed to set up file logging")

    logger.info(f"Logging configured: level={level}, file={log_to_file}")
