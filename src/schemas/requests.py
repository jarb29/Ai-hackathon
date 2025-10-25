"""Pydantic data models for web audit request structures.

This module defines the input data schema for audit requests using Pydantic
models. Provides type validation and URL format validation for incoming
audit requests via the REST API.
"""

from pydantic import BaseModel, HttpUrl, Field


class AuditRequest(BaseModel):
    """Web audit request model.
    
    Simple request structure requiring only a target URL.
    Automatically validates URL format (must be valid HTTP/HTTPS).
    """
    url: HttpUrl = Field(
        description="Target website URL to audit (must be valid HTTP/HTTPS)",
        examples=["https://example.com", "https://www.google.com"]
    )