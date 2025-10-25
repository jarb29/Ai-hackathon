from fastapi import APIRouter, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
import httpx

router = APIRouter()
templates = Jinja2Templates(directory="frontend/templates")


@router.get("/web", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@router.post("/web/audit", response_class=HTMLResponse)
async def audit(request: Request, url: str = Form(...)):
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "http://localhost:9000/audit",
                json={"url": url},
                timeout=60.0
            )
            if response.status_code == 200:
                result = response.json()
            else:
                # Handle error responses
                try:
                    error_data = response.json()
                    error_msg = error_data.get('detail', 'Unknown error')
                except:
                    error_msg = response.text
                raise Exception(f"API Error ({response.status_code}): {error_msg}")
        
        return templates.TemplateResponse("result.html", {
            "request": request,
            "result": result,
            "url": url
        })
    except Exception as e:
        return templates.TemplateResponse("index.html", {
            "request": request,
            "error": str(e)
        })