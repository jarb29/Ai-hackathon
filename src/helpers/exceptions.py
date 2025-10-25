class AuditException(Exception):
    """Base exception for audit operations"""
    pass


class MCPConnectionError(AuditException):
    """MCP server connection error"""
    pass


class LLMAnalysisError(AuditException):
    """LLM analysis error"""
    pass


class InvalidURLError(AuditException):
    """Invalid URL error"""
    pass