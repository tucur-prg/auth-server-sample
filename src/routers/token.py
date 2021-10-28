from typing import Optional

from fastapi import APIRouter, Form, Header, Depends

import logging

from service.grants import ServiceFactory, GrantsService
from service.user_service import UserService
from exception import UnauthorizedClientException
from models.auth import AuthModel, get_auth_model
from models.client import ClientModel, get_client_model
from util.id_gen import random_string

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

    code = random_string(5)

    auth_model.saveCode(code, client_id, user.username, scope)

    return {
        "code": code,
    }

@router.post("/v1/token", tags=["token"])
async def token(
    logic: GrantsService = Depends(ServiceFactory)
):
    logic.validation()

    return logic.generate_token()