"""FastAPI route handlers for web audit endpoints.

This module defines the REST API endpoints for performing web audits.
It handles HTTP requests, validates input, delegates to business logic,
and returns structured audit responses.
"""

from fastapi import APIRouter, Depends, HTTPException
from schemas.requests import AuditRequest
from schemas.responses import AuditResponse
from business.audit_logic import AuditService
from helpers.validators import validate_url
from clients.service_factory import get_audit_service
from utils.logger import get_logger

logger = get_logger(__name__)

router = APIRouter()


@router.post(
    "/audit",
    response_model=AuditResponse,
    summary="Perform Web Audit",
    description="""Analyze website performance and security with AI-powered insights.
    
    **Input**: Single URL to audit
    **Output**: Complete audit report including:
    - Core Web Vitals (LCP, FID, CLS)
    - Lighthouse performance score
    - Security headers analysis
    - Vulnerability assessment
    - Executive business summary
    - Prioritized recommendations
    
    **Example Request**:
    ```json
    {"url": "https://example.com"}
    ```
    """,
    tags=["Audit"]
)
async def perform_audit(
    request: AuditRequest,
    audit_service: AuditService = Depends(get_audit_service)
) -> AuditResponse:
    """Perform comprehensive web audit on target URL.
    
    REST API endpoint that accepts a URL and returns a complete audit report
    including performance metrics, security assessment, and recommendations.
    
    Args:
        request: AuditRequest containing target URL
        audit_service: Injected AuditService for business logic
        
    Returns:
        AuditResponse: Structured audit results with performance, security,
                      and recommendation data
                      
    Raises:
        HTTPException: 500 if audit fails due to invalid URL or system error
    """
    try:
        logger.info("[audit_request] Starting audit for URL: %s", request.url)
        
        # Validate URL format and accessibility
        validate_url(str(request.url))
        logger.info("✓ URL validation passed")
        
        # Delegate to business service for complete audit pipeline
        result = await audit_service.perform_audit(str(request.url))
        
        # DEBUG: Log the result to see if executive_summary is present
        logger.info(f"[debug] Audit result has executive_summary: {hasattr(result, 'executive_summary')}")
        if hasattr(result, 'executive_summary'):
            logger.info(f"[debug] Executive summary content: {result.executive_summary}")
        
        logger.info("✓ Audit completed successfully")
        return result
        
    except Exception as e:
        logger.error("[audit_routes] Audit failed: %s", str(e), exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))