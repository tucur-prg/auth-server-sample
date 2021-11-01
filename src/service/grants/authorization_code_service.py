
from exception import (
    InvalidRequestException,
    InvalidGrantException,
    UnauthorizedClientException,
    TokenExpiredException
)
from .grants_service import GrantsService

from entity.oauth import Token, RefreshToken

class AuthorizationCodeService(GrantsService):
    GRANT_TYPE = "authorization_code"

    def __init__(self, client_id, code):
        if not code:
            raise InvalidRequestException("code not found.")

        self.client_id = client_id
        self.code = code

    def validation(self):
        res = self.model.readCode(self.code)
        if not res:
            raise InvalidGrantException("The authorization code is not found.")

        if not res.equals(self.client_id):
            raise UnauthorizedClientException()
            
        if res.isExpired():
            raise TokenExpiredException()

    def generate_token(self):
        res = self.model.readCode(self.code)

        access_token = Token(client_id=res.client_id, username=res.username, scope=res.scope)
        refresh_token = RefreshToken(client_id=res.client_id, username=res.username, scope=res.scope)

        self.model.saveToken(access_token)
        self.model.saveRefreshToken(refresh_token)
        self.model.removeCode(self.code)

        return {
            "access_token": access_token.key,
            "token_type": "Bearer",
            "expire_in": access_token.expire_in,
            "refresh_token": refresh_token.key,
        }
