from typing import Optional
import logging
import httpx
import jwt

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

logger = logging.getLogger("uvicorn")

app = FastAPI()

templates = Jinja2Templates(directory="templates")

credential = ("client001", "secret987")

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
    id_token: Optional[str] = None,
    state: Optional[str] = None,
    error: Optional[str] = None,
):
    token = None
    token_payload = {}

    if code:
        async with httpx.AsyncClient() as client:
            response = await client.post('http://provider:8080/v1/token', auth=credential, data = {
                "grant_type": "authorization_code",
                "code": code,
            })

        res = response.json()
        if "error" in res:
            error = res["error"]
        else:
            token = res["access_token"]

        if "id_token" in res:
            token_payload = jwt.decode(res["id_token"], "secret", algorithms=["HS256"], audience="client001")

    code_payload = {}
    if id_token:
        code_payload = jwt.decode(id_token, "secret", algorithms=["HS256"], audience="client001")

    return templates.TemplateResponse("cb.j2", {
        "request": request,
        "state": state,
        "error": error,
        "token": token,
        "code_payload": code_payload,
        "token_payload": token_payload,
    })
