"""
Logging utility for log_wizard.

Provides consistent logging configuration across the application.
"""

import logging
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional


def setup_logging(log_level: int = logging.INFO,
                 log_to_file: bool = False,
                 log_dir: Optional[str] = None) -> logging.Logger:
    """
    Set up logging configuration.

    Args:
        log_level: Logging level (default: INFO)
        log_to_file: Whether to log to file in addition to console
        log_dir: Directory for log files (creates timestamped folder if None)

    Returns:
        Configured logger instance
    """
    # Create logger
    logger = logging.getLogger()
    logger.setLevel(log_level)

    # Remove existing handlers
    logger.handlers.clear()

    # Create formatter
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(log_level)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # File handler (optional)
    if log_to_file:
        if log_dir is None:
            timestamp = datetime.now().strftime('%Y%m%d-%H%M%S')
            log_dir = f'output/{timestamp}'

        log_dir_path = Path(log_dir)
        log_dir_path.mkdir(parents=True, exist_ok=True)

        log_file = log_dir_path / 'log_wizard.log'
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setLevel(log_level)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

        logger.info(f"Logging to file: {log_file}")

    return logger
