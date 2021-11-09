from typing import Optional
import logging

from fastapi import Depends, Form

from exception import InvalidRequestException

from .grants_service import GrantsService

from service.client_service import ClientService
from service.user_service import UserService

from models.auth import get_auth_model

from entity.oauth import Token, RefreshToken

logger = logging.getLogger("uvicorn")

GRANT_TYPE = "password"

def validation(
    grant_type: Optional[str] = Form(None),
    username: Optional[str] = Form(None),
    password: Optional[str] = Form(None),
    scope: Optional[str] = Form(None),
):
    if grant_type == GRANT_TYPE and not username:
        raise InvalidRequestException("username not found.")

    if grant_type == GRANT_TYPE and not password:
        raise InvalidRequestException("password not found.")

class ResourceOwnerService(GrantsService):
    def __init__(
        self,
        scope: Optional[str] = Form(None),
        client: ClientService = Depends(ClientService),
        user: UserService = Depends(UserService),
        model: dict = Depends(get_auth_model),
    ):
        self.scope = scope
        self.client = client
        self.user = user
        self.model = model

    def verify(self):
        self.client.verify()
        self.user.verify()

    def generate_token(self):
        token_args = {
            "client_id": self.client.client_id,
            "username": self.user.username,
            "scope": self.scope,
        }

        access_token = Token(**token_args)
        refresh_token = RefreshToken(**token_args)

        self.model.saveToken(access_token)
        self.model.saveRefreshToken(refresh_token)

        return {
            "access_token": access_token.key,
            "token_type": "Bearer",
            "expire_in": access_token.expire_in,
            "refresh_token": refresh_token.key,
        }
