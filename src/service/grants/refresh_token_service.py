
from exception import (
    InvalidRequestException,
    InvalidGrantException,
    UnauthorizedClientException,
    TokenExpiredException
)
from .grants_service import GrantsService

from entity.oauth import Token, RefreshToken

class RefreshTokenService(GrantsService):
    GRANT_TYPE = "refresh_token"

    def __init__(self, client_id, refresh_token):
        if not refresh_token:
            raise InvalidRequestException("refresh_token not found.")

        self.client_id = client_id
        self.refresh_token = refresh_token

    def validation(self):
        refresh_token = self.model.readRefreshToken(self.refresh_token)
        if not refresh_token:
            raise InvalidGrantException("Token has been expired or revoked.")

        if not refresh_token.equals(self.client_id):
            raise UnauthorizedClientException()

        if refresh_token.isExpired():
            raise TokenExpiredException()

    def generate_token(self):
        res = self.model.readRefreshToken(self.refresh_token)

        access_token = Token(client_id=res.client_id, username=res.username, scope=res.scope)
        refresh_token = RefreshToken(client_id=res.client_id, username=res.username, scope=res.scope)

        self.model.saveToken(access_token)
        self.model.saveRefreshToken(refresh_token)
        self.model.removeRefreshToken(self.refresh_token)

        return {
            "access_token": access_token.key,
            "token_type": "Bearer",
            "expire_in": access_token.expire_in,
            "refresh_token": refresh_token.key,
        }
