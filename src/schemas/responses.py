from typing import Dict, List, Optional, Any
from pydantic import BaseModel


class PerformanceMetrics(BaseModel):
    lighthouse_score: Optional[int] = None
    core_web_vitals: Dict[str, Any] = {}
    ttfb: Optional[float] = None
    fcp: Optional[float] = None
    lcp: Optional[float] = None
    cls: Optional[float] = None


class SecurityAssessment(BaseModel):
    risk_level: str = "unknown"
    https_enabled: bool = False
    security_headers: Dict[str, bool] = {}
    vulnerabilities: List[str] = []


class ExecutiveSummary(BaseModel):
    business_impact: str = ""
    investment_priority: str = "medium"
    roi_estimate: str = ""
    timeline: str = ""
    key_recommendations: List[str] = []


class AuditResponse(BaseModel):
    url: str
    status: str = "completed"
    performance: PerformanceMetrics
    security: SecurityAssessment
    executive_summary: ExecutiveSummary
    technical_details: Dict[str, Any] = {}
    timestamp: str