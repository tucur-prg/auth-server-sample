from typing import Optional
import base64
import logging

from fastapi import Header, Depends

from exception import UnauthorizedClientException

from models.client import get_client_model

logger = logging.getLogger("uvicorn")

class ClientService:
    def __init__(
        self,
        authorization: Optional[str] = Header(""),
        model: dict = Depends(get_client_model)
    ):
        res = authorization.split(" ")
        if res[0].lower() != "basic":
            raise UnauthorizedClientException()

        client_id, client_secret = base64.urlsafe_b64decode(res[1]).decode("utf-8").split(":")

        self.client_id = client_id
        self.client_secret = client_secret
        self.model = model

    def verify(self):
        client = self.model.readClient(self.client_id)
        if not client:
            raise UnauthorizedClientException()
        
        if  not client.equals(self.client_secret):
            raise UnauthorizedClientException()

        return True
