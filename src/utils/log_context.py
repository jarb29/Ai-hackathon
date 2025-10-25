"""Logging context management for correlation tracking and performance monitoring.

This module provides thread-safe context managers for tracking request correlation IDs,
execution timing, and memory usage across the audit pipeline. Essential for debugging
distributed operations and monitoring system performance.
"""

import time
import uuid
import psutil
import threading
from contextlib import contextmanager
from typing import Optional
from utils.logger import get_logger

logger = get_logger(__name__)

class LogContext:
    """Thread-safe context manager for correlation IDs and performance tracking.
    
    Provides context managers for:
    - Correlation ID tracking across async operations
    - Execution timing for performance monitoring
    - Memory usage tracking for resource optimization
    
    Uses thread-local storage to maintain context isolation
    between concurrent audit requests.
    """
    
    _local = threading.local()
    
    @classmethod
    def get_correlation_id(cls) -> Optional[str]:
        """Get correlation ID for current thread.
        
        Returns:
            Optional[str]: Current correlation ID or None if not set
        """
        return getattr(cls._local, 'correlation_id', None)
    
    @classmethod
    def set_correlation_id(cls, correlation_id: str) -> None:
        """Set correlation ID for current thread.
        
        Args:
            correlation_id: Unique identifier for request tracking
        """
        cls._local.correlation_id = correlation_id
    
    @classmethod
    @contextmanager
    def correlation_id(cls, correlation_id: str = None):
        """Context manager for request correlation tracking.
        
        Automatically generates correlation ID if not provided and ensures
        proper cleanup when context exits. Used by middleware to track
        requests across the audit pipeline.
        
        Args:
            correlation_id: Optional correlation ID (auto-generated if None)
            
        Yields:
            str: The correlation ID being used for this context
        """
        if correlation_id is None:
            correlation_id = str(uuid.uuid4())[:8]
        
        old_id = cls.get_correlation_id()
        cls.set_correlation_id(correlation_id)
        try:
            yield correlation_id
        finally:
            if old_id:
                cls.set_correlation_id(old_id)
            else:
                cls._local.correlation_id = None
    
    @classmethod
    @contextmanager
    def timer(cls, operation_name: str):
        """Context manager for operation timing and memory tracking.
        
        Measures execution time and memory usage for performance monitoring.
        Logs start/completion with timing data and memory delta.
        
        Args:
            operation_name: Human-readable name for the operation being timed
            
        Example:
            with log_context.timer("Complete Audit Pipeline"):
                result = await audit_service.perform_audit(url)
        """
        start_time = time.time()
        start_memory = cls._get_memory_usage()
        
        logger.info("Starting %s", operation_name)
        logger.debug("[memory] Initial usage: %.1f MB", start_memory)
        
        try:
            yield
        finally:
            end_time = time.time()
            end_memory = cls._get_memory_usage()
            execution_time = end_time - start_time
            
            logger.info("✓ %s completed in %.2fs", operation_name, execution_time)
            logger.debug("[memory] Final usage: %.1f MB (delta: %.1f MB)", 
                        end_memory, end_memory - start_memory)
    
    @classmethod
    @contextmanager
    def memory_tracker(cls):
        """Context manager for detailed memory usage monitoring.
        
        Tracks memory usage before and after operations for resource
        optimization and leak detection.
        
        Example:
            with log_context.memory_tracker():
                large_operation()
        """
        initial_memory = cls._get_memory_usage()
        logger.info("Initial memory usage: %.1f MB", initial_memory)
        
        try:
            yield
        finally:
            final_memory = cls._get_memory_usage()
            logger.info("Final memory usage: %.1f MB", final_memory)
    
    @classmethod
    def _get_memory_usage(cls) -> float:
        """Get current process memory usage in megabytes.
        
        Returns:
            float: Memory usage in MB, or 0.0 if unable to determine
        """
        try:
            process = psutil.Process()
            return process.memory_info().rss / 1024 / 1024
        except Exception:
            return 0.0

# Global log context instance for application-wide use
log_context = LogContext()