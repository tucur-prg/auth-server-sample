from models.model import Model, get_connection

from entity.token import Token, RefreshToken

class AuthModel(Model):
    def saveCode(self, code, client_id, username, scope):
        self.set(self.getKey("codes", code), {
            "code": code,
            "client_id": client_id,
            "username": username,
            "scope": scope,
        })

    def readCode(self, code):
        return self.get(self.getKey("codes", code))

    def removeCode(self, code):
        self.delete(self.getKey("codes", code))

    def saveToken(self, grant_type: str, token: Token):
        self.set(self.getKey("tokens", token.key), {
            "grant_type": grant_type,
            "token": token.__dict__,
        })

    def readToken(self, token):
        res = self.get(self.getKey("tokens", token))
        if not res:
            return None

        return {
            "grant_type": res["grant_type"],
            "token": Token(**res["token"])
        }

    def saveRefreshToken(self, refresh_token):
        self.set(self.getKey("refresh_tokens", refresh_token.key), refresh_token.__dict__)

    def readRefreshToken(self, refresh_token):
        res = self.get(self.getKey("refresh_tokens", refresh_token))
        if not res:
            return None

        return RefreshToken(**res)

    def removeRefreshToken(self, refresh_token):
        self.delete(self.getKey("refresh_tokens", refresh_token))

def get_auth_model():
    return AuthModel(get_connection())
