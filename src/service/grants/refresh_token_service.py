from typing import Optional
import logging

from fastapi import Depends, Form

from exception import InvalidRequestException

from .grants_service import GrantsService

from service.client_service import ClientService
from service.refresh_token_service import RefreshTokenService as TokenServce

from models.auth import get_auth_model

from entity.oauth import Token, RefreshToken

logger = logging.getLogger("uvicorn")

GRANT_TYPE = "refresh_token"

def validation(
    grant_type: Optional[str] = Form(None),
    refresh_token: Optional[str] = Form(None),
):
    if grant_type == GRANT_TYPE and not refresh_token:
        raise InvalidRequestException("refresh_token not found.")

class RefreshTokenService(GrantsService):
    def __init__(
        self,
        client: ClientService = Depends(ClientService),
        token: TokenServce = Depends(TokenServce),
        model: dict = Depends(get_auth_model),
    ):
        self.client = client
        self.token = token
        self.model = model

    def verify(self):
        self.client.verify()
        self.token.verify()

    def generate_token(self):
        res = self.model.readRefreshToken(self.token.refresh_token)

        token_args = {
            "client_id": res.client_id,
            "username": res.username,
            "scope": res.scope,
        }

        access_token = Token(**token_args)
        refresh_token = RefreshToken(**token_args)

        self.model.saveToken(access_token)
        self.model.saveRefreshToken(refresh_token)
        self.model.removeRefreshToken(self.token.refresh_token)

        return {
            "access_token": access_token.key,
            "token_type": "Bearer",
            "expire_in": access_token.expire_in,
            "refresh_token": refresh_token.key,
        }
