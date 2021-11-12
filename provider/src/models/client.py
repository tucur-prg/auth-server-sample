from models.model import Model, get_connection
from entity.client import Client

class ClientModel(Model):
    def saveClient(self, client: Client):
        self.set(self.getKey("clients", client.client_id), client.dict())

    def readClient(self, client_id):
        res = self.get(self.getKey("clients", client_id))
        if not res:
            return None
        return Client(**res)

def get_client_model():
    return ClientModel(get_connection())
