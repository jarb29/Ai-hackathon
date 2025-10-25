"""OpenAI LLM client for AI-powered web audit analysis.

This module provides the LLMClient class that integrates OpenAI's GPT models
with Chrome DevTools MCP tools to perform intelligent web audits. It coordinates
between AI analysis and browser automation to generate comprehensive audit reports.

Three-Phase Architecture:
OpenAI Call 1 → Browser Tools → OpenAI Call 2 → OpenAI Call 3 → Complete Report

1. OpenAI Function Calling: AI selects which browser tools to use
2. OpenAI Structured Outputs: AI analyzes results and generates detailed audit
3. OpenAI Executive Summary: AI creates C-suite business impact summary
"""

import json
import uuid
from datetime import datetime
from openai import AsyncOpenAI
from schemas.responses import AuditResponse, ExecutiveSummary
from prompts.prompts import get_audit_analysis_prompt, get_web_audit_expert_prompt, get_structured_audit_prompt, get_executive_summary_prompt
from config.config import settings
from utils.logger import get_logger

logger = get_logger(__name__)


class LLMClient:
    """OpenAI client for AI-powered web audit analysis.

    This client integrates OpenAI's GPT models with MCP tools to perform
    intelligent web audits. It uses function calling to coordinate browser
    automation and AI analysis for comprehensive performance and security assessment.
    """

    def __init__(self, api_key: str, model: str = None):
        """Initialize the OpenAI client.

        Args:
            api_key: OpenAI API key for authentication
            model: GPT model to use (defaults to config setting)
        """
        self.client = AsyncOpenAI(api_key=api_key)
        self.model = model or settings.openai_model  # Use config default if not specified
        logger.info(f"[llm_client] Initialized with model: {self.model}")
        logger.info(f"[llm_client] Using OpenAI Structured Outputs with Pydantic schema")

    async def analyze_with_mcp_tools(self, url: str, mcp_client) -> AuditResponse:
        """Perform AI-powered web audit using MCP tools.

        Coordinates between OpenAI GPT model and Chrome DevTools MCP tools:
        1. Gets available MCP tools for browser automation
        2. Uses OpenAI function calling to determine which tools to use
        3. Executes browser automation via MCP client
        4. Analyzes results with AI to generate structured audit report
        5. Creates executive summary with business impact analysis

        Args:
            url: Target website URL to audit
            mcp_client: MCP client for Chrome DevTools browser automation

        Returns:
            AuditResponse: Complete audit with performance metrics, security assessment,
                         recommendations, and executive summary for C-suite reporting

        Raises:
            Exception: If OpenAI API calls or MCP tool execution fails
        """
        # Get filtered MCP tools to reduce OpenAI function calling complexity
        tools = await self._get_essential_tools(mcp_client)

        # Use expert system prompts for specialized web audit analysis
        system_prompt = get_web_audit_expert_prompt()
        user_prompt = get_structured_audit_prompt(url)

        # OpenAI Call #1: Function Calling - AI selects browser tools to execute
        logger.info(f"[llm_call_1] → Starting OpenAI Call #1 (Function Calling) for {url}")
        response = await self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            tools=tools,
            tool_choice=settings.llm_tool_choice,  # Configurable tool selection strategy
            temperature=settings.llm_temperature  # Configurable randomness control
        )
        logger.info(f"[llm_call_1] ← Completed OpenAI Call #1 - Selected {len(response.choices[0].message.tool_calls or [])} tools")

        # Execute MCP tools based on OpenAI function calling decisions
        tool_results = {}
        if response.choices[0].message.tool_calls:
            for tool_call in response.choices[0].message.tool_calls:
                tool_name = tool_call.function.name
                tool_args = json.loads(tool_call.function.arguments)
                result = await mcp_client.call_tool(tool_name, tool_args)
                tool_results[tool_name] = result

        # OpenAI Call #2: Structured Outputs - AI analyzes data and generates audit report
        analysis_prompt = get_audit_analysis_prompt(url, tool_results)
        logger.info(f"[llm_call_2] → Starting OpenAI Call #2 (Structured Analysis) for {url}")
        logger.info(f"[structured_outputs] Starting Pydantic structured analysis for {url}")

        # Generate schema directly from Pydantic model
        schema = AuditResponse.model_json_schema()
        logger.info(f"[structured_outputs] Generated schema with {len(schema['properties'])} properties")

        final_response = await self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": analysis_prompt}],
            response_format={
                "type": "json_schema",
                "json_schema": {
                    "name": "audit_response",
                    "strict": True,
                    "schema": schema
                }
            },
            temperature=settings.llm_temperature
        )
        logger.info(f"[llm_call_2] ← Completed OpenAI Call #2 - Generated structured audit report")

        # Handle refusal detection
        if hasattr(final_response.choices[0].message, 'refusal') and final_response.choices[0].message.refusal:
            logger.warning(f"[structured_outputs] Model refused: {final_response.choices[0].message.refusal}")
            raise Exception(f"Model refused request: {final_response.choices[0].message.refusal}")

        # Parse and validate with Pydantic
        content = final_response.choices[0].message.content
        logger.debug(f"[structured_outputs] Response length: {len(content)} chars")

        result_json = json.loads(content)

        # Add required fields if missing (schema should prevent this)
        if "audit_id" not in result_json:
            result_json["audit_id"] = str(uuid.uuid4())
        if "timestamp" not in result_json:
            result_json["timestamp"] = datetime.utcnow().isoformat()

        # OpenAI Call #3: Executive Summary - Generate C-suite business summary
        executive_prompt = get_executive_summary_prompt(result_json)
        logger.info(f"[llm_call_3] → Starting OpenAI Call #3 (Executive Summary) for {url}")
        logger.info(f"[executive_summary] Generating C-suite summary for {url}")
        
        executive_schema = ExecutiveSummary.model_json_schema()
        
        executive_response = await self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": executive_prompt}],
            response_format={
                "type": "json_schema",
                "json_schema": {
                    "name": "executive_summary",
                    "strict": True,
                    "schema": executive_schema
                }
            },
            temperature=0.3  # Lower temperature for executive consistency
        )
        
        executive_content = executive_response.choices[0].message.content
        executive_json = json.loads(executive_content)
        
        # LOG THE THIRD CALL OUTPUT
        logger.info(f"[llm_call_3] ← Completed OpenAI Call #3 - Executive Summary Generated")
        logger.info(f"[llm_call_3] Executive Summary Output: {executive_json}")
        
        result_json["executive_summary"] = executive_json
        
        # DEBUG: Log the complete result_json before creating AuditResponse
        logger.info(f"[debug] Complete result_json keys: {list(result_json.keys())}")
        logger.info(f"[debug] Executive summary in result_json: {result_json.get('executive_summary')}")
        
        audit_response = AuditResponse(**result_json)
        
        # DEBUG: Log the final audit_response to see if executive_summary is preserved
        logger.info(f"[debug] Final audit_response has executive_summary: {hasattr(audit_response, 'executive_summary')}")
        if hasattr(audit_response, 'executive_summary'):
            logger.info(f"[debug] Final executive_summary content: {audit_response.executive_summary}")
        
        logger.info(f"[executive_summary] ✓ Complete audit with executive summary - Score: {audit_response.overall_score}")
        return audit_response

    async def _get_essential_tools(self, mcp_client) -> list:
        """Return only essential audit tools to reduce choice complexity"""
        all_tools = await mcp_client.get_available_tools()

        # Use configurable essential tools list
        essential_tool_names = set(settings.essential_tools)  # Convert to set for faster lookup

        return [tool for tool in all_tools
                if tool["function"]["name"] in essential_tool_names]



