"""HTTP-based MCP client for multi-container architecture.

This module provides the HTTPMCPClient class that communicates with the Chrome MCP
service via HTTP REST API instead of subprocess communication. This enables
proper service separation in a multi-container Docker environment.
"""

import aiohttp
import asyncio
from typing import Dict, Any, List
from config.config import settings
from utils.logger import get_logger

logger = get_logger(__name__)


class HTTPMCPClient:
    """HTTP-based MCP client for multi-container architecture.
    
    This client communicates with the Chrome MCP service via HTTP REST API,
    enabling proper service separation and independent scaling in a 
    multi-container Docker environment.
    """
    
    def __init__(self, mcp_service_url: str = None):
        """Initialize HTTP MCP client.
        
        Args:
            mcp_service_url: URL of the MCP service (defaults to config setting)
        """
        self.mcp_service_url = mcp_service_url or settings.mcp_service_url
        self.session = None
        self.timeout = aiohttp.ClientTimeout(total=settings.mcp_service_timeout)
        logger.info(f"[http_mcp_client] Initialized with service URL: {self.mcp_service_url}")
    
    async def __aenter__(self):
        """Async context manager entry."""
        self.session = aiohttp.ClientSession(timeout=self.timeout)
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        if self.session:
            await self.session.close()
    
    async def get_available_tools(self) -> List[Dict[str, Any]]:
        """Get available MCP tools from the service.
        
        Returns:
            List of OpenAI function definitions for available MCP tools
            
        Raises:
            Exception: If service communication fails
        """
        if not self.session:
            self.session = aiohttp.ClientSession(timeout=self.timeout)
        
        url = f"{self.mcp_service_url}/mcp/tools"
        
        try:
            logger.info("[http_mcp_client] Fetching available tools from MCP service")
            async with self.session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    tools = data.get('tools', [])
                    
                    # Convert to OpenAI function calling format
                    openai_tools = []
                    for tool in tools:
                        openai_tool = {
                            "type": "function",
                            "function": {
                                "name": tool["name"],
                                "description": tool.get("description", ""),
                                "parameters": tool.get("inputSchema", {"type": "object", "properties": {}})
                            }
                        }
                        openai_tools.append(openai_tool)
                    
                    logger.info(f"[http_mcp_client] Retrieved {len(openai_tools)} tools from MCP service")
                    return openai_tools
                else:
                    error_text = await response.text()
                    raise Exception(f"Failed to get tools from MCP service: {response.status} - {error_text}")
        except asyncio.TimeoutError:
            raise Exception(f"Timeout getting tools from MCP service: {url}")
        except Exception as e:
            logger.error(f"[http_mcp_client] Failed to get available tools: {e}")
            raise
    
    async def call_tool(self, tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Execute MCP tool via HTTP API.
        
        Args:
            tool_name: Name of MCP tool to execute
            arguments: Tool-specific arguments as dictionary
            
        Returns:
            Dictionary containing tool execution results
            
        Raises:
            Exception: If tool execution fails
        """
        if not self.session:
            self.session = aiohttp.ClientSession(timeout=self.timeout)
        
        url = f"{self.mcp_service_url}/mcp/tools/{tool_name}"
        payload = {"arguments": arguments}
        
        logger.info(f"[http_mcp_client] Executing tool: {tool_name}")
        logger.debug(f"[http_mcp_client] Tool arguments: {arguments}")
        
        try:
            import time
            start_time = time.time()
            
            async with self.session.post(url, json=payload) as response:
                duration = time.time() - start_time
                
                if response.status == 200:
                    result = await response.json()
                    if result.get('success'):
                        logger.info(f"[http_mcp_client] ✓ Tool {tool_name} completed in {duration:.2f}s")
                        return result.get('result', {})
                    else:
                        error_msg = result.get('error', 'Unknown error')
                        raise Exception(f"MCP tool execution failed: {error_msg}")
                else:
                    error_text = await response.text()
                    raise Exception(f"MCP service error: {response.status} - {error_text}")
                    
        except asyncio.TimeoutError:
            raise Exception(f"MCP tool {tool_name} timed out after {settings.mcp_service_timeout}s")
        except Exception as e:
            logger.error(f"[http_mcp_client] Tool execution failed: {e}")
            raise Exception(f"MCP tool execution failed: {str(e)}")
    
    async def health_check(self) -> bool:
        """Check if MCP service is healthy.
        
        Returns:
            True if service is healthy, False otherwise
        """
        if not self.session:
            self.session = aiohttp.ClientSession(timeout=self.timeout)
        
        url = f"{self.mcp_service_url}/health"
        
        try:
            async with self.session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    return data.get('status') == 'healthy'
                return False
        except Exception as e:
            logger.warning(f"[http_mcp_client] Health check failed: {e}")
            return False