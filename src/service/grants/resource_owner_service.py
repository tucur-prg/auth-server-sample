
from exception import InvalidRequestException
from .grants_service import GrantsService

from entity.token import Token, RefreshToken

class ResourceOwnerService(GrantsService):
    GRANT_TYPE = "password"

    def __init__(self, client_id, username, scope):
        if not username:
            raise InvalidRequestException("username not found.")

        # password のチェックどこでやるか？

        self.client_id = client_id
        self.username = username
        self.scope = scope

    def validation(self):
        pass

    def generate_token(self):
        token = Token(client_id=self.client_id, username=self.username, scope=self.scope)
        refresh_token = RefreshToken(client_id=self.client_id, username=self.username, scope=self.scope)

        self.model.saveToken(self.GRANT_TYPE, token)
        self.model.saveRefreshToken(refresh_token)

        return {
            "access_token": token.key,
            "token_type": "Bearer",
            "expire_in": token.expire_in,
            "refresh_token": refresh_token.key,
        }
