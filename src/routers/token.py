from typing import Optional

from fastapi import APIRouter, Form, Header, Depends

import logging

from service.grants import ServiceFactory, GrantsService
from service.user_service import UserService
from exception import UnauthorizedClientException
from models.auth import AuthModel, get_auth_model
from models.client import ClientModel, get_client_model
from entity.oauth import Code

logger = logging.getLogger("uvicorn")

router = APIRouter()

@router.post("/v1/code", tags=["token"])
async def code(
    client_id: str = Form(...),
    scope: Optional[str] = Form(None),
    user: UserService = Depends(UserService),
    auth_model: AuthModel = Depends(get_auth_model),
    client_model: ClientModel = Depends(get_client_model),
):
    client = client_model.getClient(client_id)
    if not client:
        raise UnauthorizedClientException()

    user.verify()
    
    code = Code(client_id=client_id, username=user.username, scope=scope)

    auth_model.saveCode(code)

    return {
        "code": code.key,
        "expire_in": code.expire_in,
    }

@router.post("/v1/token", tags=["token"])
async def token(
    logic: GrantsService = Depends(ServiceFactory)
):
    logic.validation()

    return logic.generate_token()
