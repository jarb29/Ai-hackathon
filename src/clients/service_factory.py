"""Dependency injection factory for service instances.

This module provides factory functions for creating and configuring service
instances with proper dependency injection. It centralizes service creation
and ensures consistent configuration across the application.
"""

import os
from config.config import settings
from clients.mcp_tool_client import MCPToolClient
from clients.http_mcp_client import HTTPMCPClient
from clients.llm_client import LLMClient
from business.audit_logic import AuditService


def get_mcp_client():
    """Create appropriate MCP client based on environment.
    
    Factory function that detects the deployment environment and returns
    the appropriate MCP client:
    - HTTPMCPClient for Docker/containerized environments
    - MCPToolClient for local development
    
    Returns:
        MCP client instance (HTTPMCPClient or MCPToolClient)
    """
    # Check if running in Docker environment
    is_docker = os.getenv('ENVIRONMENT') == 'development' and 'chrome-mcp' in settings.mcp_service_url
    
    if is_docker:
        # Use HTTP client for multi-container Docker setup
        return HTTPMCPClient(settings.mcp_service_url)
    else:
        # Use subprocess client for local development
        return MCPToolClient()


def get_llm_client() -> LLMClient:
    """Create OpenAI LLM client instance with configuration.
    
    Factory function for creating LLM client with API key and model
    settings from application configuration.
    
    Returns:
        LLMClient: Configured OpenAI client for AI-powered analysis
    """
    return LLMClient(settings.openai_api_key, settings.openai_model)


def get_audit_service() -> AuditService:
    """Create complete audit service with all dependencies.
    
    Factory function that creates and wires together all components needed
    for web audits: MCP client for browser automation, LLM client for AI
    analysis, and the audit service that coordinates between them.
    
    Used by FastAPI dependency injection to provide AuditService instances
    to route handlers.
    
    Returns:
        AuditService: Fully configured audit service with all dependencies
    """
    # Create and inject dependencies for complete audit pipeline
    mcp_client = get_mcp_client()  # Chrome DevTools browser automation
    llm_client = get_llm_client()  # OpenAI AI-powered analysis
    return AuditService(mcp_client, llm_client)