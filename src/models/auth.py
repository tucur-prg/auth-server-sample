from models.model import Model, get_connection

from entity.oauth import Code, Token, RefreshToken

class AuthModel(Model):
    def saveCode(self, code):
        self.set(self.getKey("codes", code.key), code.__dict__)

    def readCode(self, code):
        res = self.get(self.getKey("codes", code))
        if not res:
            return None

        return Code(**res)

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
