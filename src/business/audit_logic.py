from datetime import datetime
from typing import Dict, Any
from src.clients.mcp_tool_client import MCPToolClient
from src.clients.llm_client import LLMClient
from src.schemas.responses import AuditResponse, PerformanceMetrics, SecurityAssessment, ExecutiveSummary
from src.config.config import settings
from src.utils.logger import setup_logger

logger = setup_logger(__name__)


class AuditService:
    def __init__(self):
        self.mcp_client = MCPToolClient(settings.mcp_server_path, settings.mcp_server_args)
        self.llm_client = LLMClient()

    async def perform_audit(self, url: str) -> AuditResponse:
        """Orchestrate the complete three-phase audit process"""
        logger.info(f"Starting audit for {url}")
        
        try:
            # Start MCP server
            await self.mcp_client.start_server()
            
            # Phase 1: AI-driven tool selection and execution
            tool_results = await self._execute_browser_tools(url)
            
            # Phase 2: Technical analysis
            technical_report = await self.llm_client.create_technical_report(url, tool_results)
            
            # Phase 3: Executive summary
            executive_data = await self.llm_client.create_executive_summary(technical_report)
            
            # Build response
            response = self._build_audit_response(url, technical_report, executive_data, tool_results)
            
            logger.info(f"Audit completed for {url}")
            return response
            
        except Exception as e:
            logger.error(f"Audit failed for {url}: {e}")
            raise
        finally:
            await self.mcp_client.stop_server()

    async def _execute_browser_tools(self, url: str) -> Dict[str, Any]:
        """Execute browser automation tools to gather data"""
        results = {}
        
        try:
            # Navigate to page
            results["navigation"] = await self.mcp_client.navigate_page(url)
            
            # Start performance tracing
            await self.mcp_client.performance_start_trace()
            
            # Security checks via JavaScript
            security_script = """
            ({
                https: location.protocol === 'https:',
                headers: {
                    csp: !!document.querySelector('meta[http-equiv="Content-Security-Policy"]'),
                    xframe: true // Would need server response headers
                },
                certificates: location.protocol === 'https:'
            })
            """
            results["security"] = await self.mcp_client.evaluate_script(security_script)
            
            # Performance metrics
            perf_script = """
            ({
                timing: performance.timing,
                navigation: performance.navigation,
                entries: performance.getEntriesByType('navigation')[0] || {},
                vitals: {
                    fcp: performance.getEntriesByName('first-contentful-paint')[0]?.startTime,
                    lcp: performance.getEntriesByType('largest-contentful-paint')[0]?.startTime
                }
            })
            """
            results["performance"] = await self.mcp_client.evaluate_script(perf_script)
            
            # Stop performance tracing
            results["trace"] = await self.mcp_client.performance_stop_trace()
            
            # Network analysis
            results["network"] = await self.mcp_client.list_network_requests()
            
            # Console messages
            results["console"] = await self.mcp_client.list_console_messages()
            
            # Screenshot
            results["screenshot"] = await self.mcp_client.take_screenshot()
            
        except Exception as e:
            logger.error(f"Browser tool execution failed: {e}")
            results["error"] = str(e)
        
        return results

    def _build_audit_response(self, url: str, technical_report: Dict, executive_data: Dict, tool_results: Dict) -> AuditResponse:
        """Build the final audit response"""
        
        # Extract performance data
        perf_data = technical_report.get("performance", {})
        performance = PerformanceMetrics(
            lighthouse_score=perf_data.get("lighthouse_score"),
            core_web_vitals=perf_data.get("core_web_vitals", {}),
            ttfb=perf_data.get("ttfb"),
            fcp=perf_data.get("fcp"),
            lcp=perf_data.get("lcp"),
            cls=perf_data.get("cls")
        )
        
        # Extract security data
        sec_data = technical_report.get("security", {})
        security = SecurityAssessment(
            risk_level=sec_data.get("risk_level", "unknown"),
            https_enabled=sec_data.get("https_enabled", False),
            security_headers=sec_data.get("security_headers", {}),
            vulnerabilities=sec_data.get("vulnerabilities", [])
        )
        
        # Extract executive summary
        exec_data = executive_data.get("executive_summary", {})
        executive_summary = ExecutiveSummary(
            business_impact=exec_data.get("business_impact", ""),
            investment_priority=exec_data.get("investment_priority", "medium"),
            roi_estimate=exec_data.get("roi_estimate", ""),
            timeline=exec_data.get("timeline", ""),
            key_recommendations=exec_data.get("key_recommendations", [])
        )
        
        return AuditResponse(
            url=url,
            status="completed",
            performance=performance,
            security=security,
            executive_summary=executive_summary,
            technical_details=tool_results,
            timestamp=datetime.now().isoformat()
        )