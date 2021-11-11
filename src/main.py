from typing import Optional
import logging

from fastapi import FastAPI, Depends, Form, Request
from fastapi.responses import JSONResponse

from exception import AuthException
from routers import web, token, api

logger = logging.getLogger("uvicorn")

app = FastAPI(
    title="Auth Sample"
)

app.include_router(web.router)
app.include_router(token.router)
app.include_router(api.router)

@app.exception_handler(AuthException)
async def auth_exception_handler(request: Request, e: AuthException):
    return JSONResponse(
        status_code = e.getStatusCode(),
        content = {
            "error": e.getError(),
            "error_description": e.getDescription(),
        },
    )

@app.get("/health")
async def health():
    return {"text": "OK"}


import jwt
from util.jwt import MyJWT

@app.get("/test")
async def test():
    token = jwt.encode({"some": "payloads"}, "secret", algorithm="HS256")    
    logger.info(MyJWT.decode(token, "secret"))
    logger.info(MyJWT.encode({"some": "payloads"}, "secret", algorithm="HS256"))
    logger.info(token)

    return {}

from models.user import get_user_model
from entity.user import User

@app.post("/user/register")
async def user_register(
    username: str = Form(...),
    user_model: dict = Depends(get_user_model),
):
    password = "Passw0rd"

    user = User(**{
        "username": username,
    })

    user_model.saveUser(user)

    return {
        "username": user.username,
        "password": user.password,
    }

from models.client import get_client_model
from entity.client import Client

@app.post("/client/register")
async def client_register(
    client_id: str = Form(...),
    name: str = Form(...),
    redirect_uri: str = Form(...),
    type: Optional[str] = Form("public", regex="^(public|confidential)$"),
    client_model: dict = Depends(get_client_model),
):
    client = Client(**{
        "client_id": client_id,
        "name": name,
        "type": type,
        "redirect_uri": redirect_uri,
    })

    client_model.saveClient(client)
    
    return {
        "name": client.name,
        "client_id": client.client_id,
        "client_secret": client.client_secret,
        "type": client.type,
    }
