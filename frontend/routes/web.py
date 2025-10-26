import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from fastapi import APIRouter, Request, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from pathlib import Path

router = APIRouter()

# Get project root directory - go up from frontend/routes/web.py to project root
project_root = Path(__file__).parent.parent.parent
templates_dir = project_root / "frontend" / "templates"
templates = Jinja2Templates(directory=str(templates_dir))

@router.get("/", response_class=HTMLResponse)
async def executive_dashboard(request: Request):
    """Executive Dashboard - Enterprise-Grade Interface"""
    return templates.TemplateResponse("index.html", {"request": request})

@router.get("/docs", response_class=HTMLResponse)
async def custom_redoc(request: Request):
    """Custom ReDoc API Documentation with Enterprise Styling"""
    return templates.TemplateResponse("redoc.html", {"request": request})

# Note: Report viewing is handled by JavaScript frontend calling /audit API directly
# No separate report route needed - all data flows through the main audit API