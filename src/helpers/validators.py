import re
from urllib.parse import urlparse


def is_valid_url(url: str) -> bool:
    """Validate URL format"""
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except Exception:
        return False


def sanitize_url(url: str) -> str:
    """Sanitize and normalize URL"""
    url = url.strip()
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url
    return url