from typing import Optional

from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

import logging
import httpx

from models.auth import get_auth_model
from models.client import get_client_model

logger = logging.getLogger("uvicorn")

router = APIRouter()

templates = Jinja2Templates(directory="templates")

@router.get("/authorization", response_class=HTMLResponse, include_in_schema=False)
async def authorization(
    request: Request,
    client_id: str,
    response_type: str,
    redirect_uri: Optional[str] = None,
    scope: Optional[str] = None,
    state: Optional[str] = None,
):    
    '''
    response_type: スペース区切り
        code
        token
        id_token
    '''
    logger.info(response_type.split(' '))

    return templates.TemplateResponse("authorization.j2", {
        "request": request,
        "client_id": client_id,
        "scope": scope,
        "state": state,
    })
    
@router.post("/decision", response_class=HTMLResponse, include_in_schema=False)
async def decision(
    request: Request,
    approved: str = Form(...),
    client_id: Optional[str] = Form(...),
    username: Optional[str] = Form(None),
    password: Optional[str] = Form(None),
    scope: Optional[str] = Form(""),
    state: Optional[str] = Form(""),
):
    # TODO: redirect_uri を client と関連づける
    base_uri = "http://localhost:8081/cb?stete=" + state
    if approved == "true":
        # TODO: token の場合は unsupported_response_type を返す

        async with httpx.AsyncClient() as client:
            response = await client.post('http://localhost:8080/v1/code', data = {
                "client_id": client_id,
                "username": username,
                "password": password,
                "scope": scope,
            })
        res = response.json()

        decision = "許可"
        if "code" in res:
            redirect_uri = base_uri + "&code=" + res["code"]

            # response_typeにid_tokenがあった場合はJWTを含める
            if False:
                redirect_uri += "&id_token="
        else:
            # 可能性： server_error, temporarily_unavailable
            redirect_uri = base_uri + "&error=" + res["error"] + "&error_description=" + res["error_description"].replace(" ", "+")

    else:
        decision = "拒否"
        redirect_uri = base_uri + "&error=access_denied&error_description=The+request+was+not+approved."

    return templates.TemplateResponse("decision.j2", {
        "request": request,
        "decision": decision,
        "redirect_uri": redirect_uri,
    })
