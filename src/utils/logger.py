"""Centralized logging system setup and configuration.

This module configures the application's multi-file logging system with
environment-based settings, colored console output, file rotation, and
custom METRIC level support. Provides the main logger factory function
used throughout the application.
"""

import logging
import logging.handlers
import sys
from pathlib import Path
from typing import Optional
from config.logging_config import logging_config, METRIC_LEVEL

class ColoredFormatter(logging.Formatter):
    """Custom formatter that adds colors to console log output.
    
    Provides color-coded log levels for better readability during development.
    Colors are only applied when console_colors is enabled in configuration.
    """
    
    COLORS = {
        'DEBUG': '\033[36m',     # Cyan
        'INFO': '\033[32m',      # Green
        'METRIC': '\033[35m',    # Magenta
        'WARNING': '\033[33m',   # Yellow
        'ERROR': '\033[31m',     # Red
        'CRITICAL': '\033[41m',  # Red background
        'RESET': '\033[0m'       # Reset
    }
    
    def format(self, record):
        if logging_config.console_colors:
            color = self.COLORS.get(record.levelname, self.COLORS['RESET'])
            record.levelname = f"{color}{record.levelname}{self.COLORS['RESET']}"
        return super().format(record)

def setup_logging(environment: str = None) -> None:
    """Configure comprehensive logging system based on environment.
    
    Sets up multiple log handlers for different purposes:
    - Console output (development only) with colors
    - Application log file (INFO+ messages)
    - Error log file (ERROR+ messages)
    - Metrics log file (METRIC level only)
    - Debug log file (development only)
    
    Args:
        environment: Target environment (development, testing, production)
                    Defaults to value from logging_config
    """
    
    env = environment or logging_config.environment
    
    # Ensure logs directory exists for file handlers
    logging_config.log_dir.mkdir(parents=True, exist_ok=True)
    
    # Configure root logger and clear any existing handlers
    root_logger = logging.getLogger()
    root_logger.handlers.clear()
    
    # Adjust log level based on deployment environment
    if env == "development":
        root_logger.setLevel(logging.DEBUG)
    elif env == "testing":
        root_logger.setLevel(logging.WARNING)
    else:  # production, staging
        root_logger.setLevel(logging.INFO)
    
    # Reduce verbosity of external library logging
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("httpcore").setLevel(logging.WARNING)
    logging.getLogger("openai").setLevel(logging.WARNING)
    logging.getLogger("urllib3").setLevel(logging.WARNING)
    logging.getLogger("requests").setLevel(logging.WARNING)
    
    # Add colored console output for development environment
    if env == "development" and logging_config.console_enabled:
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.INFO)  # Only INFO+ to console
        console_formatter = ColoredFormatter(logging_config.log_format)
        console_handler.setFormatter(console_formatter)
        root_logger.addHandler(console_handler)
    
    # Configure file-based logging handlers (skip for testing)
    if env != "testing":  # No file logging in testing
        
        # General application log with INFO and above
        app_handler = logging.handlers.RotatingFileHandler(
            logging_config.log_dir / logging_config.app_log_file,
            maxBytes=_parse_size(logging_config.max_file_size),
            backupCount=logging_config.backup_count
        )
        app_handler.setLevel(logging.INFO)
        app_handler.setFormatter(logging.Formatter(logging_config.log_format))
        root_logger.addHandler(app_handler)
        
        # Dedicated error log for ERROR and CRITICAL messages
        error_handler = logging.handlers.RotatingFileHandler(
            logging_config.log_dir / logging_config.error_log_file,
            maxBytes=_parse_size(logging_config.max_file_size),
            backupCount=logging_config.backup_count
        )
        error_handler.setLevel(logging.ERROR)
        error_handler.setFormatter(logging.Formatter(logging_config.log_format))
        root_logger.addHandler(error_handler)
        
        # Business metrics log (custom METRIC level only)
        metric_handler = logging.handlers.RotatingFileHandler(
            logging_config.log_dir / logging_config.metric_log_file,
            maxBytes=_parse_size(logging_config.max_file_size),
            backupCount=logging_config.backup_count
        )
        metric_handler.setLevel(METRIC_LEVEL)
        metric_handler.addFilter(lambda record: record.levelno == METRIC_LEVEL)
        metric_handler.setFormatter(logging.Formatter(logging_config.log_format))
        root_logger.addHandler(metric_handler)
        
        # Detailed debug log for development troubleshooting
        if env == "development":
            debug_handler = logging.handlers.RotatingFileHandler(
                logging_config.log_dir / logging_config.debug_log_file,
                maxBytes=_parse_size(logging_config.max_file_size),
                backupCount=logging_config.backup_count
            )
            debug_handler.setLevel(logging.DEBUG)
            debug_handler.setFormatter(logging.Formatter(logging_config.log_format))
            root_logger.addHandler(debug_handler)

def get_logger(name: str = None) -> logging.Logger:
    """Factory function to get configured logger instance.
    
    Main entry point for obtaining loggers throughout the application.
    Automatically sets up logging system if not already configured.
    
    Args:
        name: Logger name (typically __name__ from calling module)
              Defaults to current module name if not provided
              
    Returns:
        logging.Logger: Configured logger instance with all handlers
    """
    
    # Initialize logging system if not already configured
    if not logging.getLogger().handlers:
        setup_logging()
    
    # Create module-specific logger instance
    logger_name = name or __name__
    return logging.getLogger(logger_name)

def _parse_size(size_str: str) -> int:
    """Convert human-readable size string to bytes.
    
    Supports KB, MB, GB suffixes for file rotation configuration.
    
    Args:
        size_str: Size string like '10MB', '500KB', '1GB'
        
    Returns:
        int: Size in bytes
    """
    size_str = size_str.upper()
    if size_str.endswith('MB'):
        return int(size_str[:-2]) * 1024 * 1024
    elif size_str.endswith('KB'):
        return int(size_str[:-2]) * 1024
    elif size_str.endswith('GB'):
        return int(size_str[:-2]) * 1024 * 1024 * 1024
    else:
        return int(size_str)

# Auto-initialize logging system when module is imported
setup_logging()