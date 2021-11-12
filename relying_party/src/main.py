from typing import Optional
import logging

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

logger = logging.getLogger("uvicorn")

app = FastAPI()

templates = Jinja2Templates(directory="templates")

@app.get("/health")
async def health():
    return {"text": "OK"}

@app.get("/", response_class=HTMLResponse, include_in_schema=False)
async def top(
    request: Request,
):
    return templates.TemplateResponse("top.j2", {
        "request": request,
    })

@app.get("/cb", response_class=HTMLResponse, include_in_schema=False)
async def callback(
    request: Request,
    code: Optional[str] = None,
    state: Optional[str] = None,
    error: Optional[str] = None,
    error_description: Optional[str] = None,
):
    return templates.TemplateResponse("cb.j2", {
        "request": request,
        "code": code,
        "error": error,
    })
