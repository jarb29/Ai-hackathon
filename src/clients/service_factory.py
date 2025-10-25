"""Dependency injection factory for service instances.

This module provides factory functions for creating and configuring service
instances with proper dependency injection. It centralizes service creation
and ensures consistent configuration across the application.
"""

from config.config import settings
from clients.http_mcp_client import HTTPMCPClient
from clients.llm_client import LLMClient
from business.audit_logic import AuditService


def get_mcp_client() -> HTTPMCPClient:
    """Create HTTP-based MCP client for multi-container setup.
    
    Factory function for creating MCP client that communicates with the
    Chrome MCP service via HTTP REST API in a multi-container environment.
    
    Returns:
        HTTPMCPClient: Configured HTTP MCP client for browser automation
    """
    return HTTPMCPClient(settings.mcp_service_url)


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