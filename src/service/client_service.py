from typing import Optional
import base64

from fastapi import Header, Depends

from exception import UnauthorizedClientException

from models.client import get_client_model

class ClientService:
    def __init__(
        self,
        authorization: Optional[str] = Header(""),
        model: dict = Depends(get_client_model)
    ):
        res = authorization.split(" ")
        if res[0] != "Basic":
            raise UnauthorizedClientException()

        client_id, client_secret = base64.urlsafe_b64decode(res[1]).decode("utf-8").split(":")

        self.client_id = client_id
        self.client_secret = client_secret
        self.model = model

    def verify(self):
        client = self.model.getClient(self.client_id)
        if not client:
            raise UnauthorizedClientException()

        if client["client_secret"] != self.client_secret:
            raise UnauthorizedClientException()

        return True