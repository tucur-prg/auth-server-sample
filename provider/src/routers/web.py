from typing import Optional
import logging
import httpx

from fastapi import APIRouter, Request, Form, Depends, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

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
    nonce: Optional[str] = None,
    code_challenge: Optional[str] = None,
    code_challenge_method: Optional[str] = None,
):
    '''
    response_type: スペース区切り
        code
        token
        id_token
    '''
    return templates.TemplateResponse("authorization.j2", {
        "request": request,
        "client_id": client_id,
        "response_type": response_type,
        "scope": scope,
        "state": state,
        "nonce": nonce,
        "code_challenge": code_challenge,
        "code_challenge_method": code_challenge_method,
    })
    
@router.post("/decision", response_class=HTMLResponse, include_in_schema=False)
async def decision(
    request: Request,
    approved: str = Form(...),
    client_id: Optional[str] = Form(...),
    response_type: Optional[str] = Form(...),
    username: Optional[str] = Form(None),
    password: Optional[str] = Form(None),
    scope: Optional[str] = Form(""),
    state: Optional[str] = Form(""),
    nonce: Optional[str] = Form(""),
    code_challenge: Optional[str] = Form(""),
    code_challenge_method: Optional[str] = Form(""),
    client_model: dict = Depends(get_client_model),
):
    client = client_model.readClient(client_id)
    if not client:
        raise HTTPException(status_code=404, detail="client not found.")

    base_uri = client.redirect_uri + "?stete=" + state

    if approved == "true":
        response_type = response_type.split(' ')
        logger.info(response_type)

        if "code" in response_type:
            async with httpx.AsyncClient() as client:
                response = await client.post('http://localhost:8080/v1/code', data = {
                    "client_id": client_id,
                    "username": username,
                    "password": password,
                    "scope": scope,
                    "nonce": nonce,
                    "code_challenge": code_challenge,
                    "code_challenge_method": code_challenge_method,
                })
            res = response.json()
        else:
            res = {
                "error": "unsupported_response_type",
                "error_description": "",
            }

        if "code" in res:
            redirect_uri = base_uri + "&code=" + res["code"]

            if "id_token" in response_type:
                logger.info("generate code id_token.")
                async with httpx.AsyncClient() as client:
                    response = await client.post('http://localhost:8080/v1/id_token', data = {
                        "client_id": client_id,
                        "username": username,
                        "password": password,
                        "nonce": nonce,
                    })
                res = response.json()

                redirect_uri += "&id_token=" + res["id_token"]
        else:
            # 可能性： server_error, temporarily_unavailable
            redirect_uri = base_uri + "&error=" + res["error"] + "&error_description=" + res["error_description"].replace(" ", "+")

    else:
        redirect_uri = base_uri + "&error=access_denied&error_description=The+request+was+not+approved."

    return RedirectResponse(redirect_uri, status_code=301)
