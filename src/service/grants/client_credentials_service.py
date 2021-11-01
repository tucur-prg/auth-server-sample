
from .grants_service import GrantsService

from entity.oauth import Token

import logging

logger = logging.getLogger("uvicorn")

class ClientCredentialsService(GrantsService):
    GRANT_TYPE = "client_credentials"

    def __init__(self, client_id, scope):
        self.client_id = client_id
        self.scope = scope

    def validation(self):
        pass

    def generate_token(self):
        access_token = Token(client_id=self.client_id, scope=self.scope)

        self.model.saveToken(access_token)

        return {
            "access_token": access_token.key,
            "token_type": "Bearer",
            "expire_in": access_token.expire_in,
        }
