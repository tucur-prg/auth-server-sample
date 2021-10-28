from typing import Optional

from fastapi import FastAPI, Depends
from fastapi import Form, Request
from fastapi.responses import JSONResponse

import logging
import jwt

from exception import AuthException
from routers import web, token, api
from util.jwt import MyJWT

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

@app.get("/test")
async def test():
#    token = jwt.encode({"some": "payloads"}, "secret", algorithm="HS256")    
#    logger.info(MyJWT.decode(token, "secret"))
#    logger.info(MyJWT.encode({"some": "payloads"}, "secret", algorithm="HS256"))
#    logger.info(token)

    return {}

from models.user import get_user_model

@app.post("/user/register")
async def user_register(
    username: str = Form(...),
    user_model: dict = Depends(get_user_model),
):
    password = "Passw0rd"

    user_model.saveUser(username, password)

    return {
        "username": username,
        "password": password,
    }

from models.client import get_client_model

@app.post("/client/register")
async def client_register(
    client_id: str = Form(...),
    name: str = Form(...),
    type: Optional[str] = Form("public", regex="^(public|confidential)$"),
    client_model: dict = Depends(get_client_model),
):
    client_secret = "secret987"

    client_model.saveClient(client_id, client_secret, name, type)

    return {
        "name": name,
        "client_id": client_id,
        "client_secret": client_secret,
        "type": type,
    }
