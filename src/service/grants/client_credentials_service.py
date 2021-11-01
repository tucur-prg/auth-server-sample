
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
        token = Token(client_id=self.client_id, scope=self.scope)

        self.model.saveToken(self.GRANT_TYPE, token)

        return {
            "access_token": token.key,
            "token_type": "Bearer",
            "expire_in": token.expire_in,
        }
