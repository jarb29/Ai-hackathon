"""FastAPI middleware for request/response logging and correlation tracking.

This module provides HTTP middleware that adds correlation IDs to requests,
logs request/response timing and status, and tracks performance metrics
for monitoring and debugging purposes.
"""

import time
import uuid
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from utils.logger import get_logger
from utils.log_context import log_context

logger = get_logger(__name__)

class LoggingMiddleware(BaseHTTPMiddleware):
    """FastAPI middleware for request/response logging with correlation IDs"""
    
    async def dispatch(self, request: Request, call_next):
        # Generate correlation ID
        correlation_id = str(uuid.uuid4())[:8]
        
        # Start timing
        start_time = time.time()
        
        with log_context.correlation_id(correlation_id):
            # Log request start
            logger.info("[request_id=%s] %s %s started", 
                       correlation_id, request.method, request.url.path)
            
            # Add correlation ID to request state
            request.state.correlation_id = correlation_id
            
            try:
                # Process request
                response = await call_next(request)
                
                # Calculate duration
                duration = time.time() - start_time
                
                # Log successful completion
                logger.info("[request_id=%s] %s %s completed in %.2fs status=%d", 
                           correlation_id, request.method, request.url.path, 
                           duration, response.status_code)
                
                # Log performance metric
                logger.metric("[api_performance] method=%s path=%s duration=%.2fs status=%d correlation_id=%s",
                             request.method, request.url.path, duration, 
                             response.status_code, correlation_id)
                
                # Add correlation ID to response headers
                response.headers["X-Correlation-ID"] = correlation_id
                
                return response
                
            except Exception as e:
                # Calculate duration for failed requests
                duration = time.time() - start_time
                
                # Log error
                logger.error("[request_id=%s] %s %s failed in %.2fs: %s", 
                            correlation_id, request.method, request.url.path, 
                            duration, str(e), exc_info=True)
                
                raise