from models.model import Model, get_connection
from entity.user import User

class UserModel(Model):
    def saveUser(self, user: User):
        self.set(self.getKey("users", user.username), user.dict())

    def readUser(self, username):
        res = self.get(self.getKey("users", username))
        if not res:
            return None
        return User(**res)

def get_user_model():
    return UserModel(get_connection())
