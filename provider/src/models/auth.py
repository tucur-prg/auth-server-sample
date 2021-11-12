from models.model import Model, get_connection

from entity.oauth import Code, Token, RefreshToken

class AuthModel(Model):
    def saveCode(self, code: Code):
        self.set(self.getKey("codes", code.key), code.dict())

    def readCode(self, key):
        res = self.get(self.getKey("codes", key))
        if not res:
            return None

        return Code(**res)

    def removeCode(self, key):
        self.delete(self.getKey("codes", key))

    def saveToken(self, token: Token):
        self.set(self.getKey("tokens", token.key), token.dict())

    def readToken(self, key):
        res = self.get(self.getKey("tokens", key))
        if not res:
            return None

        return Token(**res)

    def saveRefreshToken(self, refresh_token: RefreshToken):
        self.set(self.getKey("refresh_tokens", refresh_token.key), refresh_token.dict())

    def readRefreshToken(self, key):
        res = self.get(self.getKey("refresh_tokens", key))
        if not res:
            return None

        return RefreshToken(**res)

    def removeRefreshToken(self, key):
        self.delete(self.getKey("refresh_tokens", key))

def get_auth_model():
    return AuthModel(get_connection())
