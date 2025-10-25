import uvicorn
from fastapi import FastAPI
from src.app.routes import audit, health
from src.config.config import settings
from src.utils.logger import setup_logger

logger = setup_logger(__name__)

app = FastAPI(
    title="Web Audit Agent",
    description="Enterprise-Grade Autonomous Web Performance & Security Auditor",
    version="1.0.0"
)

# Include API routes
app.include_router(audit.router, prefix="/api", tags=["audit"])
app.include_router(health.router, prefix="/api", tags=["health"])


if __name__ == "__main__":
    logger.info(f"Starting Web Audit Agent on {settings.app_host}:{settings.app_port}")
    uvicorn.run(
        "src.app.main:app",
        host=settings.app_host,
        port=settings.app_port,
        reload=settings.app_debug
    )