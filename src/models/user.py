from models.model import Model, get_connection

class UserModel(Model):
    def saveUser(self, username, password):
        self.set(self.getKey("users", username), {
            "username": username,
            "password": password,
        })

    def getUser(self, username):
        return self.get(self.getKey("users", username))

def get_user_model():
    return UserModel(get_connection())
