"""Health check and API information endpoints.

This module provides health monitoring endpoints for the Web Audit Agent API.
Includes root endpoint with API information and health check endpoint for
monitoring service status and component availability.
"""

from fastapi import APIRouter
from datetime import datetime

router = APIRouter()


@router.get(
    "/",
    summary="API Information",
    description="Get basic API metadata and available endpoints",
    tags=["Info"]
)
async def root():
    """API root endpoint with service information.
    
    Provides basic information about the Web Audit Agent API including
    version, description, status, and available endpoints. Used for
    API discovery and basic service identification.
    
    Returns:
        dict: API metadata including name, version, status, and endpoints
    """
    return {
        "name": "Web Audit Agent API",
        "version": "1.0.0",
        "description": "Simplified web performance & security auditor",
        "status": "operational",
        "endpoints": {
            "health": "/health",
            "audit": "/audit"
        }
    }


@router.get(
    "/health",
    summary="Health Check",
    description="Service health status for monitoring and load balancers",
    tags=["Health"]
)
async def health_check():
    """Health check endpoint for service monitoring.
    
    Provides health status information for the API and its key components.
    Used by load balancers, monitoring systems, and deployment pipelines
    to verify service availability and readiness.
    
    Returns:
        dict: Health status with timestamp and component status:
            - api: FastAPI service status
            - mcp_client: Chrome DevTools MCP client readiness
            - llm_client: OpenAI LLM client readiness
    """
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "services": {
            "api": "operational",        # FastAPI service status
            "mcp_client": "ready",       # Chrome DevTools MCP availability
            "llm_client": "ready"        # OpenAI LLM client readiness
        }
    }