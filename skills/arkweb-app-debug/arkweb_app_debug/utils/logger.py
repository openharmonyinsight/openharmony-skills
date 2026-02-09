"""Logging utilities."""

import logging
import os
import sys
from pathlib import Path
from typing import Optional


def setup_logger(
    name: str = "arkweb-app-debug",
    level: int = logging.INFO,
    log_file: Optional[str] = None,
    verbose: bool = False,
) -> logging.Logger:
    """
    Setup logger with console and optional file output.

    Args:
        name: Logger name
        level: Logging level
        log_file: Optional log file path
        verbose: Enable verbose output

    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(name)

    # Remove existing handlers
    logger.handlers.clear()

    # Set level
    if verbose:
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(level)

    # Create formatter
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # File handler
    if log_file:
        log_path = Path(log_file).expanduser()
        log_path.parent.mkdir(parents=True, exist_ok=True)

        file_handler = logging.FileHandler(log_path, encoding="utf-8")
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger


def get_logger(name: str = "arkweb-app-debug") -> logging.Logger:
    """Get existing logger or create new one."""
    return logging.getLogger(name)


# Color codes for terminal output
class Colors:
    """ANSI color codes for terminal output."""

    RESET = "\033[0m"
    RED = "\033[0;31m"
    GREEN = "\033[0;32m"
    YELLOW = "\033[1;33m"
    BLUE = "\033[0;34m"
    MAGENTA = "\033[0;35m"
    CYAN = "\033[0;36m"
    WHITE = "\033[1;37m"


def colorize(text: str, color: str) -> str:
    """Add color to text for terminal output."""
    return f"{color}{text}{Colors.RESET}"


def log_info(logger: logging.Logger, message: str) -> None:
    """Log info message with color."""
    logger.info(colorize(f"[INFO] {message}", Colors.BLUE))


def log_success(logger: logging.Logger, message: str) -> None:
    """Log success message with color."""
    logger.info(colorize(f"[SUCCESS] {message}", Colors.GREEN))


def log_warn(logger: logging.Logger, message: str) -> None:
    """Log warning message with color."""
    logger.warning(colorize(f"[WARN] {message}", Colors.YELLOW))


def log_error(logger: logging.Logger, message: str) -> None:
    """Log error message with color."""
    logger.error(colorize(f"[ERROR] {message}", Colors.RED))
