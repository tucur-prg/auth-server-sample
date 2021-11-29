from typing import Optional
import time
import logging

from fastapi import APIRouter, Form, Depends

from service.grants import (
    ServiceFactory,
    GrantsService,
    authorization_code_service,
    client_credentials_service,
    refresh_token_service,
    resource_owner_service,
    refresh_token_service,
)

from service.client_service import ClientService
from service.user_service import UserService

from models.auth import AuthModel, get_auth_model
from models.client import ClientModel, get_client_model

from entity.oauth import Code

from exception import (
    UnauthorizedClientException,
    InvalidTokenException,
    TokenExpiredException,
    InvalidRequestException
)

from util.jwt import MyJWT

logger = logging.getLogger("uvicorn")

router = APIRouter()

@router.post("/v1/code", tags=["token"])
async def code(
    client_id: str = Form(...),
    scope: Optional[str] = Form(None),
    nonce: Optional[str] = Form(None),
    user: UserService = Depends(UserService),
    auth_model: AuthModel = Depends(get_auth_model),
    client_model: ClientModel = Depends(get_client_model),
):
    client = client_model.readClient(client_id)
    if not client:
        raise UnauthorizedClientException()

    user.verify()

    code = Code(**{
        "client_id": client_id,
        "username": user.username,
        "scope": scope,
        "nonce": nonce,
    })

    auth_model.saveCode(code)

    return {
        "code": code.key,
        "expire_in": code.expire_in,
    }

@router.post("/v1/id_token", tags=["token"])
async def id_token(
    client_id: str = Form(...),
    nonce: Optional[str] = Form(None),
    user: UserService = Depends(UserService),
    client_model: ClientModel = Depends(get_client_model),
):
    client = client_model.readClient(client_id)
    if not client:
        raise UnauthorizedClientException()

    user.verify()

    payload = {
        "iss": "http://localhost:8080",
        "sub": user.username,
        "aud": client_id,
        "exp": int(time.time()) + 3600,
        "iat": int(time.time()),
        "auth_time": int(time.time()),
        "nonce": nonce,
    }

    return {
        "id_token": MyJWT.encode(payload, "secret", algorithm="HS256"),
    }

@router.post("/v1/token", tags=["token"], dependencies=[
    Depends(authorization_code_service.validation),
    Depends(resource_owner_service.validation),
    Depends(refresh_token_service.validation),
    Depends(client_credentials_service.validation),
])
async def token(
    logic: GrantsService = Depends(ServiceFactory)
):
    logic.verify()

    return logic.generate_token()

@router.post("/v1/token/info", tags=["token"])
async def token_info(
    token: str = Form(...),
    client: ClientService = Depends(ClientService),
    model: AuthModel = Depends(get_auth_model),
):
    client.verify()

    access_token = model.readToken(token)
    if not access_token:
        raise InvalidTokenException()

    if access_token.isExpired():
        raise TokenExpiredException()
        
    if not access_token.equals(client.client_id):
        raise InvalidRequestException()

    return {
        "username": access_token.username,
        "scope": access_token.scope,
        "expire_in": access_token.expire_in,
    }
