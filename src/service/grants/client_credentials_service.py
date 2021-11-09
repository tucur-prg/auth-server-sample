from typing import Optional
import logging

from fastapi import Depends, Form

from .grants_service import GrantsService

from service.client_service import ClientService

from models.auth import get_auth_model

from entity.oauth import Token

logger = logging.getLogger("uvicorn")

GRANT_TYPE = "client_credentials"

def validation():
    pass

class ClientCredentialsService(GrantsService):
    def __init__(
        self,
        scope: Optional[str] = Form(None),
        client: ClientService = Depends(ClientService),
        model: dict = Depends(get_auth_model),
    ):
        self.scope = scope
        self.client = client
        self.model = model
        
    def verify(self):
        self.client.verify()

    def generate_token(self):
        token_args = {
            "client_id": self.client.client_id,
            "scope": self.scope,
        }

        access_token = Token(**token_args)

        self.model.saveToken(access_token)

        return {
            "access_token": access_token.key,
            "token_type": "Bearer",
            "expire_in": access_token.expire_in,
        }
