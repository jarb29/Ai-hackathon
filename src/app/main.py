"""FastAPI application entry point for Web Audit Agent.

This module configures and starts the FastAPI web server with all necessary
middleware, routes, and static file serving. It provides both REST API
endpoints and web interface for the audit system.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.routes import health, audit
from frontend.routes import web
from config.config import settings
from middleware.logging_middleware import LoggingMiddleware
from utils.logger import get_logger

logger = get_logger(__name__)

app = FastAPI(
    title="Enterprise Web Audit Platform",
    description="""## Enterprise Web Audit Platform API
    
**Simple REST API** for comprehensive web performance and security auditing.

### Available Endpoints

#### 🔍 **POST /audit**
- **Input**: `{"url": "https://example.com"}`
- **Output**: Complete audit report with performance, security, and recommendations
- **Features**: Core Web Vitals, security headers, vulnerability assessment, executive summary

#### ❤️ **GET /health**
- **Output**: Service health status and component availability
- **Use**: Monitoring, load balancer health checks

#### 📋 **GET /**
- **Output**: API information and available endpoints
- **Use**: Service discovery and API metadata

### Response Structure
```json
{
  "audit_id": "unique-audit-identifier",
  "url": "https://audited-site.com",
  "performance": {
    "core_web_vitals": {"lcp": 2.1, "fid": 45, "cls": 0.05},
    "lighthouse_score": 85,
    "overall_grade": "B"
  },
  "security": {
    "https_enabled": true,
    "risk_level": "low",
    "vulnerabilities": []
  },
  "recommendations": [],
  "executive_summary": {
    "business_impact": "Performance optimization needed",
    "investment_priority": "medium"
  }
}
```
    """,
    version="1.0.0",
    contact={
        "name": "Web Audit Platform",
        "url": "https://github.com/web-audit-platform",
    },
    license_info={
        "name": "MIT",
        "url": "https://opensource.org/licenses/MIT",
    },
    docs_url=None,
    redoc_url=None
)

# Add logging middleware first for request/response tracking
app.add_middleware(LoggingMiddleware)

# Enable CORS for web interface and API access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve static assets (CSS, JS, images) for web interface
from pathlib import Path
project_root = Path(__file__).parent.parent.parent
static_dir = project_root / "frontend" / "static"
app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")

# Register route handlers for web interface, health checks, and audit API
app.include_router(web.router, tags=["web"])
app.include_router(health.router, tags=["health"])
app.include_router(audit.router, tags=["audit"])


if __name__ == "__main__":
    import uvicorn
    logger.info("✓ Web Audit Agent starting up")
    logger.info("✓ Server configuration: %s:%d", settings.api_host, settings.api_port)
    uvicorn.run(
        "main:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=True
    )