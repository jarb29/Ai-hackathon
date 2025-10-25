import asyncio
import json
import subprocess
from typing import Dict, Any, List
from src.utils.logger import setup_logger

logger = setup_logger(__name__)


class MCPToolClient:
    def __init__(self, server_path: str, server_args: str):
        self.server_path = server_path
        self.server_args = server_args.split()
        self.process = None
        self.request_id = 0

    async def start_server(self):
        """Start the MCP server process"""
        try:
            cmd = [self.server_path] + self.server_args
            self.process = await asyncio.create_subprocess_exec(
                *cmd,
                stdin=asyncio.subprocess.PIPE,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            logger.info("MCP server started successfully")
            
            # Initialize the server
            await self._send_request("initialize", {
                "protocolVersion": "2024-11-05",
                "capabilities": {"tools": {}},
                "clientInfo": {"name": "web-audit-agent", "version": "1.0.0"}
            })
            
        except Exception as e:
            logger.error(f"Failed to start MCP server: {e}")
            raise

    async def stop_server(self):
        """Stop the MCP server process"""
        if self.process:
            self.process.terminate()
            await self.process.wait()
            logger.info("MCP server stopped")

    async def _send_request(self, method: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """Send JSON-RPC request to MCP server"""
        if not self.process:
            raise RuntimeError("MCP server not started")

        self.request_id += 1
        request = {
            "jsonrpc": "2.0",
            "id": self.request_id,
            "method": method,
            "params": params
        }

        try:
            request_data = json.dumps(request) + "\n"
            self.process.stdin.write(request_data.encode())
            await self.process.stdin.drain()

            response_data = await self.process.stdout.readline()
            response = json.loads(response_data.decode())
            
            if "error" in response:
                raise Exception(f"MCP Error: {response['error']}")
                
            return response.get("result", {})
            
        except Exception as e:
            logger.error(f"MCP request failed: {e}")
            raise

    async def navigate_page(self, url: str) -> Dict[str, Any]:
        """Navigate to a page and capture basic metrics"""
        return await self._send_request("tools/call", {
            "name": "navigate_page",
            "arguments": {"url": url}
        })

    async def performance_start_trace(self) -> Dict[str, Any]:
        """Start performance tracing"""
        return await self._send_request("tools/call", {
            "name": "performance_start_trace",
            "arguments": {}
        })

    async def performance_stop_trace(self) -> Dict[str, Any]:
        """Stop performance tracing and get metrics"""
        return await self._send_request("tools/call", {
            "name": "performance_stop_trace",
            "arguments": {}
        })

    async def evaluate_script(self, expression: str) -> Dict[str, Any]:
        """Execute JavaScript in the browser"""
        return await self._send_request("tools/call", {
            "name": "evaluate_script",
            "arguments": {"expression": expression}
        })

    async def take_screenshot(self) -> Dict[str, Any]:
        """Take a screenshot of the current page"""
        return await self._send_request("tools/call", {
            "name": "take_screenshot",
            "arguments": {}
        })

    async def list_network_requests(self) -> Dict[str, Any]:
        """Get network requests and analyze headers"""
        return await self._send_request("tools/call", {
            "name": "list_network_requests",
            "arguments": {}
        })

    async def list_console_messages(self) -> Dict[str, Any]:
        """Get console messages and errors"""
        return await self._send_request("tools/call", {
            "name": "list_console_messages",
            "arguments": {}
        })