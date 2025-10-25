from typing import List
from pydantic import BaseModel, Field


class CoreWebVitals(BaseModel):
    model_config = {"extra": "forbid"}
    
    lcp: float
    fid: float
    cls: float


class PerformanceResults(BaseModel):
    model_config = {"extra": "forbid"}
    
    core_web_vitals: CoreWebVitals
    lighthouse_score: int
    overall_grade: str


class Vulnerability(BaseModel):
    model_config = {"extra": "forbid"}
    
    name: str
    severity: str
    description: str


class SecurityResults(BaseModel):
    model_config = {"extra": "forbid"}
    
    https_enabled: bool
    csp_header: str
    hsts_header: str
    xframe_header: str
    risk_level: str
    vulnerabilities: List[Vulnerability]


class Recommendation(BaseModel):
    model_config = {"extra": "forbid"}
    
    category: str
    priority: str
    title: str
    description: str
    impact: str


class ExecutiveSummary(BaseModel):
    model_config = {"extra": "forbid"}
    
    business_impact: str
    key_risks: List[str]
    investment_priority: str
    roi_estimate: str
    action_timeline: str


class AuditResponse(BaseModel):
    """Complete web audit response with performance, security, and business insights."""
    model_config = {"extra": "forbid"}
    
    audit_id: str
    url: str
    timestamp: str
    performance: PerformanceResults
    security: SecurityResults
    recommendations: List[Recommendation]
    overall_score: int
    grade: str
    executive_summary: ExecutiveSummary