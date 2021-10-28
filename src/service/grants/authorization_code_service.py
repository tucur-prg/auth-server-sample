
from exception import InvalidRequestException, InvalidGrantException, UnauthorizedClientException
from .grants_service import GrantsService

from entity.token import Token, RefreshToken

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

        if res["client_id"] != self.client_id:
            raise UnauthorizedClientException()

    def generate_token(self):
        res = self.model.readCode(self.code)

        token = Token(client_id=res["client_id"], username=res["username"], scope=res["scope"])
        refresh_token = RefreshToken(client_id=res["client_id"], username=res["username"], scope=res["scope"])

        self.model.saveToken(self.GRANT_TYPE, token)
        self.model.saveRefreshToken(refresh_token)
        self.model.removeCode(self.code)

        return {
            "access_token": token.key,
            "token_type": "Bearer",
            "expire_in": token.expire_in,
            "refresh_token": refresh_token.key,
        }
