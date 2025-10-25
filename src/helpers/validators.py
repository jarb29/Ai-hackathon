"""URL validation utilities for web audit requests.

This module provides validation functions to ensure URLs are properly
formatted and accessible before attempting web audits. Prevents common
URL format errors and security issues.
"""

import re
from urllib.parse import urlparse
from helpers.exceptions import URLValidationError


def validate_url(url: str) -> bool:
    """Validate URL format and scheme for web audit compatibility.
    
    Checks that the URL has proper format with valid scheme and netloc.
    Only allows HTTP and HTTPS protocols for security and compatibility.
    
    Args:
        url: URL string to validate
        
    Returns:
        bool: True if URL is valid
        
    Raises:
        URLValidationError: If URL format is invalid or uses unsupported scheme
    """
    try:
        # Parse URL components
        result = urlparse(url)
        
        # Ensure URL has both scheme and network location
        if not all([result.scheme, result.netloc]):
            raise URLValidationError(url)
            
        # Only allow HTTP/HTTPS for web audit compatibility
        if result.scheme not in ['http', 'https']:
            raise URLValidationError(url)
            
        return True
    except Exception:
        # Re-raise as URLValidationError for consistent error handling
        raise URLValidationError(url)