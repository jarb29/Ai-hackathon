"""Logging system configuration for the Web Audit Agent.

This module configures the application's logging system with multiple log files,
custom log levels (including METRIC level), file rotation, and environment-based
settings. Provides structured logging for debugging, monitoring, and metrics.
"""

import os
import logging
from pathlib import Path
from pydantic_settings import BaseSettings

# Project root directory
PROJECT_ROOT = Path(__file__).parent.parent.parent
LOGS_DIR = PROJECT_ROOT / "logs"

class LoggingConfig(BaseSettings):
    """Logging configuration settings with environment variable support.
    
    Configures multiple log files for different purposes:
    - app.log: General application logs
    - error.log: Error and exception logs
    - metrics.log: Performance and business metrics
    - debug.log: Detailed debugging information
    
    Supports file rotation, retention policies, and custom log levels.
    """
    # Environment Configuration
    environment: str = os.getenv("ENVIRONMENT", "development")
    
    # Log Level Configuration (supports custom METRIC level = 25)
    log_level: str = "INFO"
    
    # Log File Names and Directory Configuration
    log_dir: Path = LOGS_DIR
    app_log_file: str = "app.log"
    error_log_file: str = "error.log"
    metric_log_file: str = "metrics.log"
    debug_log_file: str = "debug.log"
    
    # File Rotation and Retention Settings
    max_file_size: str = "10MB"
    backup_count: int = 5
    retention_days: int = 30
    error_retention_days: int = 90
    
    # Log Message Format Configuration
    log_format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    date_format: str = "%Y-%m-%d %H:%M:%S"
    
    # Console Output Configuration
    console_enabled: bool = True
    console_colors: bool = True
    
    class Config:
        env_prefix = "LOG_"

# Add custom METRIC level for business and performance metrics
METRIC_LEVEL = 25
logging.addLevelName(METRIC_LEVEL, "METRIC")

def metric(self, message, *args, **kwargs):
    """Custom logging method for business and performance metrics.
    
    Logs at METRIC level (25) which is between INFO (20) and WARNING (30).
    Used for tracking audit completion times, performance scores, and
    business intelligence data.
    
    Args:
        message: Log message format string
        *args: Message format arguments
        **kwargs: Additional logging keyword arguments
    """
    if self.isEnabledFor(METRIC_LEVEL):
        self._log(METRIC_LEVEL, message, args, **kwargs)

# Extend Logger class with custom metric method
logging.Logger.metric = metric

# Global logging configuration instance
logging_config = LoggingConfig()