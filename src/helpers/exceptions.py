"""Custom exception classes for web audit error handling.

This module defines application-specific exceptions that extend FastAPI's
HTTPException to provide structured error responses with appropriate
HTTP status codes for different failure scenarios.
"""

from fastapi import HTTPException


class AuditError(HTTPException):
    """Base exception class for all web audit related errors.
    
    Extends FastAPI's HTTPException to provide consistent error handling
    across the audit system with proper HTTP status codes.
    """
    
    def __init__(self, detail: str, status_code: int = 500):
        """Initialize audit error with message and HTTP status code.
        
        Args:
            detail: Human-readable error description
            status_code: HTTP status code (defaults to 500 Internal Server Error)
        """
        super().__init__(status_code=status_code, detail=detail)


class URLValidationError(AuditError):
    """Exception raised when URL validation fails.
    
    Used when the provided URL is malformed, uses unsupported protocol,
    or is otherwise invalid for web audit processing.
    """
    
    def __init__(self, url: str):
        """Initialize URL validation error with the invalid URL.
        
        Args:
            url: The invalid URL that caused the validation failure
        """
        super().__init__(f"Invalid URL: {url}", status_code=400)


class MCPConnectionError(AuditError):
    """Exception raised when MCP server connection fails.
    
    Used when the Chrome DevTools MCP server cannot be reached,
    fails to start, or encounters communication errors.
    """
    
    def __init__(self, message: str):
        """Initialize MCP connection error with failure details.
        
        Args:
            message: Specific error message describing the MCP failure
        """
        super().__init__(f"MCP connection error: {message}", status_code=503)