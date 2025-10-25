"""Chrome DevTools MCP client for browser automation.

This module provides the MCPToolClient class that connects to Chrome DevTools
via Model Context Protocol (MCP) to enable browser automation for web audits.
It manages the Node.js MCP server process and provides JSON-RPC communication.
"""

import asyncio
import json
import subprocess
from typing import Optional
from config.config import settings
from utils.logger import get_logger

logger = get_logger(__name__)


class MCPToolClient:
    """Chrome DevTools MCP client for browser automation.

    This client manages a Node.js subprocess running the Chrome DevTools MCP server
    and provides JSON-RPC communication to execute browser automation tools.
    It bridges between the Python application and Chrome browser capabilities.

    The MCP server provides tools like:
    - navigate_page: Load websites and capture metrics
    - performance_*: Measure Core Web Vitals and performance
    - evaluate_script: Run JavaScript for security checks
    - take_screenshot: Capture visual page state
    - list_network_requests: Analyze HTTP requests and headers
    """

    def __init__(self):
        """Initialize MCP client with connection state tracking."""
        self.process: Optional[subprocess.Popen] = None
        self.connected = False
        self._tools_cache: Optional[list] = None

    async def get_available_tools(self) -> list:
        """Get available MCP tools formatted for OpenAI function calling.

        Connects to MCP server if needed, retrieves available browser tools,
        and converts them to OpenAI function calling format for LLM usage.

        Returns:
            List of OpenAI function definitions for available MCP tools

        Raises:
            Exception: If MCP server connection or tool retrieval fails
        """
        if self._tools_cache:
            return self._tools_cache

        if not self.connected:
            await self._connect()

        mcp_tools = await self._get_mcp_tools()
        self._tools_cache = [self._transform_mcp_tool_to_openai(tool) for tool in mcp_tools]
        return self._tools_cache

    async def call_tool(self, tool_name: str, arguments: dict) -> dict:
        """Execute Chrome DevTools MCP tool with given arguments.

        Sends JSON-RPC request to MCP server to execute browser automation tool.
        Handles timing, logging, and error recovery for tool execution.

        Args:
            tool_name: Name of MCP tool to execute (e.g., 'navigate_page')
            arguments: Tool-specific arguments as dictionary

        Returns:
            Dictionary containing tool execution results or error information

        Raises:
            Exception: If MCP server communication fails
        """
        if not self.connected:
            await self._connect()

        logger.info("[tool=%s] Tool execution started", tool_name)
        logger.debug("[tool=%s] Arguments: %s", tool_name, arguments)

        # Use tool name directly (no mapping needed with dynamic discovery)
        mcp_tool_name = tool_name

        try:
            import time
            start_time = time.time()
            result = await self._call_mcp_tool(mcp_tool_name, arguments)
            duration = time.time() - start_time

            logger.info("[tool=%s] ✓ Tool completed in %.2fs", tool_name, duration)
            return result
        except Exception as e:
            logger.error("[mcp_client] Tool execution failed: %s (tool=%s)", str(e), tool_name)
            return {"error": str(e), "tool": tool_name}

    async def _connect(self):
        """Establish connection to Chrome DevTools MCP server.

        Starts Node.js subprocess with chrome-devtools-mcp package,
        initializes MCP protocol communication, and establishes connection.

        Raises:
            Exception: If subprocess startup or MCP initialization fails
        """
        try:
            # Start Node.js MCP server subprocess with Chrome DevTools integration
            mcp_args = [
                settings.mcp_command, '-y', settings.mcp_package,
                f'--headless={str(settings.mcp_headless).lower()}',
                f'--isolated={str(settings.mcp_isolated).lower()}'
            ]

            self.process = subprocess.Popen(
                mcp_args,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )

            # Allow MCP server time to initialize Chrome browser connection
            await asyncio.sleep(settings.mcp_startup_timeout)

            # Send MCP protocol initialization handshake
            await self._send_request({
                "jsonrpc": "2.0",
                "id": settings.mcp_init_id,
                "method": "initialize",
                "params": {
                    "protocolVersion": settings.mcp_protocol_version,
                    "capabilities": {},
                    "clientInfo": {
                        "name": settings.mcp_client_name,
                        "version": settings.mcp_client_version
                    }
                }
            })

            self.connected = True
            self._tools_cache = None  # Reset cache on new connection

        except Exception as e:
            if self.process:
                self.process.terminate()
                self.process = None
            raise Exception(f"Failed to connect to MCP: {e}")

    async def _call_mcp_tool(self, tool_name: str, arguments: dict) -> dict:
        """Execute MCP tool via JSON-RPC protocol.

        Args:
            tool_name: MCP tool name to execute
            arguments: Tool arguments dictionary

        Returns:
            Tool execution result from MCP server
        """
        request = {
            "jsonrpc": "2.0",
            "id": settings.mcp_call_id,  # Configurable JSON-RPC ID
            "method": "tools/call",
            "params": {
                "name": tool_name,
                "arguments": arguments
            }
        }

        return await self._send_request(request)

    async def _send_request(self, request: dict) -> dict:
        """Send JSON-RPC request to MCP server subprocess.

        Args:
            request: JSON-RPC request dictionary

        Returns:
            JSON-RPC response result

        Raises:
            Exception: If subprocess communication fails or returns error
        """
        if not self.process:
            raise Exception("MCP process not started")

        request_str = json.dumps(request) + '\n'
        self.process.stdin.write(request_str)
        self.process.stdin.flush()

        response_str = self.process.stdout.readline()
        if not response_str:
            raise Exception("No response from MCP server")

        response = json.loads(response_str.strip())

        if 'error' in response:
            raise Exception(f"MCP error: {response['error']}")

        return response.get('result', {})

    async def _get_mcp_tools(self) -> list:
        """Retrieve available tools from MCP server.

        Returns:
            List of MCP tool definitions from server
        """
        request = {
            "jsonrpc": "2.0",
            "id": settings.mcp_list_id,  # Configurable JSON-RPC ID
            "method": "tools/list",
            "params": {}
        }
        response = await self._send_request(request)
        return response.get('tools', [])

    def _transform_mcp_tool_to_openai(self, mcp_tool: dict) -> dict:
        """Convert MCP tool definition to OpenAI function calling format.

        Args:
            mcp_tool: MCP tool definition with name, description, inputSchema

        Returns:
            OpenAI function definition for use in function calling
        """
        return {
            "type": "function",
            "function": {
                "name": mcp_tool["name"],
                "description": mcp_tool.get("description", ""),
                "parameters": mcp_tool.get("inputSchema", {"type": "object", "properties": {}})
            }
        }


