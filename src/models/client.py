from models.model import Model, get_connection

class ClientModel(Model):
    def saveClient(self, client_id, client_secret, name, redirect_uri = None):
        self.set(self.getKey("clients", client_id), {
            "client_id": client_id,
            "client_secret": client_secret,
            "name": name,
            "redirect_uri": redirect_uri,
        })

    def getClient(self, client_id):
        return self.get(self.getKey("clients", client_id))

def get_client_model():
    return ClientModel(get_connection())
