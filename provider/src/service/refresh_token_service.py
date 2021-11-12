from typing import Optional
import logging

from fastapi import Form, Depends

from exception import (
    InvalidRequestException,
    InvalidGrantException,
    InvalidTokenException,
    TokenExpiredException,
    UnauthorizedClientException
)

from models.auth import get_auth_model

from service.client_service import ClientService

logger = logging.getLogger("uvicorn")

class RefreshTokenService:
    def __init__(
        self,
        refresh_token: Optional[str] = Form(None),
        client: ClientService = Depends(ClientService),
        model: dict = Depends(get_auth_model)
    ):
        self.refresh_token = refresh_token
        self.client_id = client.client_id
        self.model = model

    def verify(self):
        refresh_token = self.model.readRefreshToken(self.refresh_token)
        if not refresh_token:
            raise InvalidGrantException("Token has been expired or revoked.")

        if not refresh_token.equals(self.client_id):
            raise UnauthorizedClientException()

        if refresh_token.isExpired():
            raise TokenExpiredException()

        return True
