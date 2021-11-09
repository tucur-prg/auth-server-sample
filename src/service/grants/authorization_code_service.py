from typing import Optional
import logging

from fastapi import Depends, Form

from exception import InvalidRequestException

from .grants_service import GrantsService

from service.client_service import ClientService
from service.code_service import CodeService

from models.auth import get_auth_model

from entity.oauth import Token, RefreshToken

logger = logging.getLogger("uvicorn")

GRANT_TYPE = "authorization_code"

def validation(
    grant_type: Optional[str] = Form(None),
    code: Optional[str] = Form(None),
    redirect_uri: Optional[str] = Form(None),
):
    if grant_type == GRANT_TYPE and not code:
        raise InvalidRequestException("code not found.")

class AuthorizationCodeService(GrantsService):
    def __init__(
        self,
        client: ClientService = Depends(ClientService),
        code: CodeService = Depends(CodeService),
        model: dict = Depends(get_auth_model),
    ):
        self.client = client
        self.code = code
        self.model = model

    def verify(self):
        self.client.verify()
        self.code.verify()

    def generate_token(self):
        res = self.model.readCode(self.code.code)
        
        token_args = {
            "client_id": res.client_id,
            "username": res.username,
            "scope": res.scope,
        }

        access_token = Token(**token_args)
        refresh_token = RefreshToken(**token_args)

        self.model.saveToken(access_token)
        self.model.saveRefreshToken(refresh_token)
        self.model.removeCode(self.code.code)

        return {
            "access_token": access_token.key,
            "token_type": "Bearer",
            "expire_in": access_token.expire_in,
            "refresh_token": refresh_token.key,
        }
