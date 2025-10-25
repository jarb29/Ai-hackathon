from fastapi import APIRouter, HTTPException
from src.schemas.requests import AuditRequest
from src.schemas.responses import AuditResponse
from src.business.audit_logic import AuditService
from src.utils.logger import setup_logger

logger = setup_logger(__name__)
router = APIRouter()


@router.post("/audit", response_model=AuditResponse)
async def perform_audit(request: AuditRequest):
    """Perform comprehensive web audit"""
    try:
        audit_service = AuditService()
        result = await audit_service.perform_audit(str(request.url))
        return result
    except Exception as e:
        logger.error(f"Audit endpoint error: {e}")
        raise HTTPException(status_code=500, detail=str(e))