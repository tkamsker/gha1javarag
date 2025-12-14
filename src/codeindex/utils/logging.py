"""
Structured logging setup for Java Codebase Indexer Pipeline.

Supports levels: DEBUG, INFO, WARNING, ERROR
Respects LOG_LEVEL environment variable
"""
import logging
import sys
from typing import Optional


def setup_logging(level: Optional[str] = None, verbose: bool = False) -> logging.Logger:
    """
    Setup structured logging with consistent format.

    Args:
        level: Logging level (DEBUG, INFO, WARNING, ERROR). If None, reads from LOG_LEVEL env var.
        verbose: If True, force DEBUG level and show more details

    Returns:
        Configured root logger
    """
    # Determine logging level
    if verbose:
        log_level = logging.DEBUG
    elif level:
        log_level = getattr(logging, level.upper(), logging.INFO)
    else:
        import os
        level_str = os.getenv("LOG_LEVEL", "INFO").upper()
        log_level = getattr(logging, level_str, logging.INFO)

    # Configure root logger
    logging.basicConfig(
        level=log_level,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        handlers=[
            logging.StreamHandler(sys.stderr)
        ],
        force=True  # Override any existing configuration
    )

    # Reduce noise from verbose libraries
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("httpcore").setLevel(logging.WARNING)
    logging.getLogger("urllib3").setLevel(logging.WARNING)
    logging.getLogger("weaviate").setLevel(logging.INFO)

    logger = logging.getLogger("codeindex")
    logger.setLevel(log_level)

    return logger


def get_logger(name: str) -> logging.Logger:
    """
    Get a logger for a specific module.

    Args:
        name: Module name (typically __name__)

    Returns:
        Logger instance
    """
    return logging.getLogger(f"codeindex.{name}")
