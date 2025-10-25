from typing import Dict, Any, List
from openai import AsyncOpenAI
from src.config.config import settings
from src.utils.logger import setup_logger

logger = setup_logger(__name__)


class LLMClient:
    def __init__(self):
        self.client = AsyncOpenAI(api_key=settings.openai_api_key)

    async def analyze_with_tools(self, url: str, available_tools: List[Dict]) -> List[Dict]:
        """Phase 1: AI selects and calls browser tools"""
        system_prompt = """You are a web audit expert. Analyze the given URL using available browser tools.
        Select the most appropriate tools to gather comprehensive performance and security data.
        Focus on Core Web Vitals, security headers, and overall site health."""

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Audit this website: {url}"}
        ]

        try:
            response = await self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=messages,
                tools=available_tools,
                tool_choice="auto"
            )
            
            tool_calls = []
            if response.choices[0].message.tool_calls:
                for tool_call in response.choices[0].message.tool_calls:
                    tool_calls.append({
                        "name": tool_call.function.name,
                        "arguments": tool_call.function.arguments
                    })
            
            return tool_calls
            
        except Exception as e:
            logger.error(f"LLM tool analysis failed: {e}")
            return []

    async def create_technical_report(self, url: str, tool_results: Dict[str, Any]) -> Dict[str, Any]:
        """Phase 2: Create structured technical audit report"""
        system_prompt = """You are a technical web audit analyst. Create a comprehensive technical report
        based on browser tool results. Focus on performance metrics, security assessment, and technical recommendations.
        Return structured JSON with performance, security, and technical_details sections."""

        user_prompt = f"""
        Analyze these browser tool results for {url}:
        {tool_results}
        
        Create a technical audit report with:
        1. Performance metrics (Core Web Vitals, scores)
        2. Security assessment (HTTPS, headers, vulnerabilities)
        3. Technical recommendations
        
        Return as structured JSON.
        """

        try:
            response = await self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                response_format={"type": "json_object"}
            )
            
            import json
            return json.loads(response.choices[0].message.content)
            
        except Exception as e:
            logger.error(f"Technical report generation failed: {e}")
            return {}

    async def create_executive_summary(self, technical_report: Dict[str, Any]) -> Dict[str, Any]:
        """Phase 3: Create executive summary with business impact"""
        system_prompt = """You are a business technology consultant. Create an executive summary
        that translates technical findings into business impact, ROI estimates, and strategic recommendations
        for C-suite decision makers."""

        user_prompt = f"""
        Based on this technical audit report:
        {technical_report}
        
        Create an executive summary with:
        1. Business impact assessment
        2. Investment priority (high/medium/low)
        3. ROI estimates and timelines
        4. Key strategic recommendations
        
        Return as structured JSON with executive_summary section.
        """

        try:
            response = await self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                response_format={"type": "json_object"}
            )
            
            import json
            return json.loads(response.choices[0].message.content)
            
        except Exception as e:
            logger.error(f"Executive summary generation failed: {e}")
            return {}