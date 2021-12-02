from typing import Optional
import logging

from fastapi import Form, Depends

from exception import (
    InvalidRequestException,
    InvalidGrantException,
    InvalidTokenException,
    TokenExpiredException
)

from models.auth import get_auth_model

from service.client_service import ClientService

logger = logging.getLogger("uvicorn")

class CodeService:
    def __init__(
        self,
        code: Optional[str] = Form(None),
        redirect_uri: Optional[str] = Form(None),
        code_verifier: Optional[str] = Form(None),
        client: ClientService = Depends(ClientService),
        model: dict = Depends(get_auth_model)
    ):
        self.code = code
        self.redirect_uri = redirect_uri
        self.code_verifier = code_verifier
        self.client_id = client.client_id
        self.model = model

    def verify(self):
        code = self.model.readCode(self.code)
        if not code:
            raise InvalidGrantException("The provided access grant is invalid, expired, or revoked (e.g. invalid assertion, expired authorization token, bad end-user password credentials, or mismatching authorization code and redirection URI)")

        if not code.equals(self.client_id):
            raise InvalidGrantException("The provided access grant is invalid, expired, or revoked (e.g. invalid assertion, expired authorization token, bad end-user password credentials, or mismatching authorization code and redirection URI)")

        if code.isExpired():
            raise InvalidGrantException("The provided access grant is invalid, expired, or revoked (e.g. invalid assertion, expired authorization token, bad end-user password credentials, or mismatching authorization code and redirection URI)")

        if not code.validatePKCE(self.code_verifier):
            raise InvalidGrantException("The provided access grant is invalid, expired, or revoked (e.g. invalid assertion, expired authorization token, bad end-user password credentials, or mismatching authorization code and redirection URI)")
