"""Application configuration management using Pydantic settings.

This module defines all configuration settings for the Web Audit Agent,
including API server settings, OpenAI LLM configuration, MCP server settings,
and essential tools configuration. Settings are loaded from environment
variables and .env file with type validation.
"""

import os
from pathlib import Path
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

# Get the project root directory (two levels up from this file)
PROJECT_ROOT = Path(__file__).parent.parent.parent
ENV_FILE = PROJECT_ROOT / ".env"

# Load the .env file
load_dotenv(ENV_FILE)

class Settings(BaseSettings):
    """Application settings with environment variable support.
    
    Pydantic settings class that loads configuration from environment variables
    and .env file. Provides type validation and default values for all
    application settings including API, LLM, and MCP configuration.
    
    Environment variables can override defaults (e.g., OPENAI_API_KEY).
    """
    # FastAPI Server Configuration
    api_host: str = "0.0.0.0"
    api_port: int = 9000

    # Multi-container MCP Service Configuration
    mcp_service_url: str = "http://chrome-mcp:3001"  # MCP service URL for multi-container setup
    mcp_service_timeout: int = 60  # HTTP timeout for MCP service calls
    mcp_service_retries: int = 3  # Number of retry attempts for MCP service

    # OpenAI LLM Configuration
    openai_api_key: str
    openai_model: str = "gpt-4o-mini"  # GPT model for audit analysis
    
    # OpenAI API Behavior and Performance Settings
    llm_temperature: float = 0.1  # Low temperature for consistent, deterministic audit results
    llm_tool_choice: str = "auto"  # Let LLM automatically choose which tools to use
    llm_timeout: int = 120  # Maximum seconds to wait for LLM response
    llm_max_retries: int = 3  # Number of retry attempts on LLM API failures
    
    # Chrome DevTools MCP Tools - Essential browser automation functions
    essential_tools: list = [
        "navigate_page",  # Navigate to target URL - required for all audits
        "performance_start_trace",  # Begin performance measurement - Core Web Vitals
        "performance_stop_trace",  # End performance measurement - get results
        "evaluate_script",  # Run JavaScript for security checks - HTTPS, headers, OWASP
        "take_snapshot",  # Capture DOM structure - required for element interaction
        "list_network_requests",  # Analyze HTTP requests - resource optimization
        "emulate_network",  # Test mobile performance - 3G/4G simulation
        "list_console_messages",  # Check for errors - security violations, JS errors
        "take_screenshot"  # Visual documentation - executive reporting
    ]
    
    # Node.js MCP Server Process Configuration
    mcp_server_path: str = "npx"  # Command to run MCP server
    mcp_server_args: str = "@modelcontextprotocol/server-chrome-devtools"  # MCP server package
    mcp_command: str = "npx"  # Command to run MCP server
    mcp_package: str = "chrome-devtools-mcp@latest"  # NPM package for Chrome DevTools MCP
    mcp_headless: bool = True  # Run Chrome in headless mode for server environments
    mcp_isolated: bool = True  # Run Chrome in isolated mode for security
    mcp_startup_timeout: int = 2  # Seconds to wait for MCP server startup
    
    # Model Context Protocol Communication Settings
    mcp_protocol_version: str = "2024-11-05"  # MCP protocol version for compatibility
    mcp_client_name: str = "web-audit-agent"  # Client identifier for MCP server
    mcp_client_version: str = "1.0.0"  # Client version for debugging/logging
    
    # MCP Connection Management and Error Handling
    mcp_connection_timeout: int = 30  # Seconds to wait for initial connection
    mcp_max_retries: int = 3  # Number of retry attempts on MCP failures
    mcp_retry_delay: float = 1.0  # Seconds between retry attempts
    mcp_request_timeout: int = 60  # Seconds to wait for individual tool responses
    
    # JSON-RPC Protocol IDs for MCP Communication
    mcp_init_id: int = 1  # JSON-RPC ID for initialization requests
    mcp_call_id: int = 2  # JSON-RPC ID for tool call requests
    mcp_list_id: int = 3  # JSON-RPC ID for tool list requests



    class Config:
        env_file = str(ENV_FILE)
        env_file_encoding = 'utf-8'


settings = Settings()