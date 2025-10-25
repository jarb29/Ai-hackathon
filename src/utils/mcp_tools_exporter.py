"""MCP tools documentation exporter utility.

This utility connects to the Chrome DevTools MCP server, retrieves all available
tools, and generates comprehensive documentation including tool descriptions,
parameters, and OpenAI function calling formats. Used for debugging, documentation,
and understanding MCP capabilities.
"""

import asyncio
import json
from datetime import datetime
from pathlib import Path
import sys
import os

# Add src to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from clients.mcp_tool_client import MCPToolClient


async def export_mcp_tools():
    """Export comprehensive MCP tools documentation to text file.
    
    Connects to Chrome DevTools MCP server, retrieves all available tools,
    and generates detailed documentation including:
    - Raw MCP tool definitions with schemas
    - OpenAI function calling format transformations
    - Tool categorization and analysis
    - Export summary and metadata
    
    Returns:
        str: Path to generated documentation file
        
    Raises:
        Exception: If MCP server connection or tool retrieval fails
    """
    
    # Initialize MCP client
    mcp_client = MCPToolClient()
    
    try:
        # Get available tools
        print("Connecting to MCP server...")
        tools = await mcp_client.get_available_tools()
        
        # Get raw MCP tools for detailed info
        raw_tools = await mcp_client._get_mcp_tools()
        
        # Generate filename with current date
        current_date = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"mcp_tools_documentation_{current_date}.txt"
        
        # Create docs directory if it doesn't exist
        docs_dir = Path(__file__).parent.parent.parent / "docs"
        docs_dir.mkdir(parents=True, exist_ok=True)
        
        filepath = docs_dir / filename
        
        # Generate report content
        content = generate_report_content(raw_tools, tools, current_date)
        
        # Write to file
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✅ MCP tools exported successfully to: {filepath}")
        print(f"📊 Total tools found: {len(raw_tools)}")
        
        return str(filepath)
        
    except Exception as e:
        print(f"❌ Error exporting MCP tools: {e}")
        raise
    finally:
        # Cleanup MCP connection
        if mcp_client.process:
            mcp_client.process.terminate()


def generate_report_content(raw_tools: list, openai_tools: list, export_date: str) -> str:
    """Generate comprehensive formatted documentation content.
    
    Creates detailed documentation including tool descriptions, schemas,
    OpenAI function formats, categorization, and export metadata.
    
    Args:
        raw_tools: List of raw MCP tool definitions from server
        openai_tools: List of tools transformed to OpenAI function format
        export_date: Timestamp of export generation
        
    Returns:
        str: Complete formatted documentation content
    """
    
    content = f"""
# MCP Tools Export Report
Generated on: {export_date}
Total Tools: {len(raw_tools)}

{'='*80}
CHROME DEVTOOLS MCP SERVER - AVAILABLE TOOLS
{'='*80}

"""
    
    for i, tool in enumerate(raw_tools, 1):
        content += f"""
{i}. {tool.get('name', 'Unknown Tool')}
{'-' * (len(str(i)) + 2 + len(tool.get('name', 'Unknown Tool')))}

Description: {tool.get('description', 'No description available')}

Input Schema:
{json.dumps(tool.get('inputSchema', {}), indent=2)}

"""
    
    content += f"""
{'='*80}
OPENAI FUNCTION FORMAT (FOR LLM INTEGRATION)
{'='*80}

"""
    
    for i, tool in enumerate(openai_tools, 1):
        func = tool.get('function', {})
        content += f"""
{i}. {func.get('name', 'Unknown')}
{'-' * (len(str(i)) + 2 + len(func.get('name', 'Unknown')))}

Description: {func.get('description', 'No description')}

Parameters:
{json.dumps(func.get('parameters', {}), indent=2)}

"""
    
    content += f"""
{'='*80}
EXPORT SUMMARY
{'='*80}

Export Date: {export_date}
MCP Server: chrome-devtools-mcp@latest
Protocol Version: 2024-11-05
Client: web-audit-agent v1.0.0

Tool Categories Detected:
"""
    
    # Categorize tools by functionality for better organization
    categories = set()
    for tool in raw_tools:
        name = tool.get('name', '')
        if 'navigate' in name.lower():
            categories.add('Navigation')
        elif 'screenshot' in name.lower() or 'capture' in name.lower():
            categories.add('Screenshot/Capture')
        elif 'performance' in name.lower() or 'metrics' in name.lower():
            categories.add('Performance')
        elif 'security' in name.lower():
            categories.add('Security')
        elif 'dom' in name.lower() or 'element' in name.lower():
            categories.add('DOM Manipulation')
        else:
            categories.add('Other')
    
    for category in sorted(categories):
        content += f"- {category}\n"
    
    content += f"""
Total Available Tools: {len(raw_tools)}
Successfully Transformed: {len(openai_tools)}

This export can be used for:
- Understanding available MCP capabilities
- LLM function calling integration
- Tool documentation and reference
- Debugging MCP connections

{'='*80}
"""
    
    return content


if __name__ == "__main__":
    asyncio.run(export_mcp_tools())