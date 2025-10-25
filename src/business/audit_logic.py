"""Business logic for web audit operations.

This module contains the core AuditService class that orchestrates the complete
web audit pipeline by coordinating between the LLM client and MCP tool client
to perform comprehensive performance and security analysis.
"""

from clients.mcp_tool_client import MCPToolClient
from clients.llm_client import LLMClient
from schemas.responses import AuditResponse
from utils.logger import get_logger
from utils.log_context import log_context

logger = get_logger(__name__)


class AuditService:
    """Core business service for orchestrating web audits.
    
    This service acts as the main coordinator between the OpenAI LLM client
    and Chrome DevTools MCP client to perform comprehensive web audits.
    It handles the complete audit pipeline from URL input to structured response.
    """
    
    def __init__(self, mcp_client: MCPToolClient, llm_client: LLMClient):
        """Initialize the audit service with required clients.
        
        Args:
            mcp_client: Chrome DevTools MCP client for browser automation
            llm_client: OpenAI client for AI-powered analysis
        """
        self.mcp_client = mcp_client
        self.llm_client = llm_client
    
    async def perform_audit(self, url: str) -> AuditResponse:
        """Perform comprehensive web audit on the given URL.
        
        Orchestrates the complete audit pipeline:
        1. Delegates to LLM client for AI-powered analysis
        2. LLM client uses MCP tools for browser automation
        3. Collects performance metrics (Core Web Vitals, Lighthouse)
        4. Performs security assessment (HTTPS, headers, vulnerabilities)
        5. Returns structured audit response with recommendations
        
        Args:
            url: Target website URL to audit
            
        Returns:
            AuditResponse: Structured audit results with performance,
                         security metrics, and recommendations
                         
        Raises:
            Exception: If audit pipeline fails at any stage
        """
        with log_context.timer("Complete Audit Pipeline"):
            logger.info("✓ Pipeline started")
            logger.info("[audit_url=%s] Starting comprehensive web audit", url)
            
            try:
                # Delegate to LLM client which coordinates MCP tool usage
                audit_result = await self.llm_client.analyze_with_mcp_tools(
                    url=url,
                    mcp_client=self.mcp_client
                )
                
                # Log business metrics
                logger.metric("[audit_completed] url=%s overall_score=%d grade=%s", 
                             url, audit_result.overall_score, audit_result.grade)
                
                logger.metric("[core_web_vitals] url=%s LCP=%.2fs FID=%.0fms CLS=%.3f", 
                             url, audit_result.performance.core_web_vitals.lcp,
                             audit_result.performance.core_web_vitals.fid,
                             audit_result.performance.core_web_vitals.cls)
                
                logger.metric("[security_assessment] url=%s https_enabled=%s risk_level=%s vulnerabilities=%d", 
                             url, audit_result.security.https_enabled,
                             audit_result.security.risk_level,
                             len(audit_result.security.vulnerabilities))
                
                logger.info("✓ Audit completed successfully")
                return audit_result
                
            except Exception as e:
                logger.error("[audit_logic] Audit failed for URL %s: %s", url, str(e), exc_info=True)
                raise
