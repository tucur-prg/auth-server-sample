from typing import Optional

from fastapi import Form, Header, Depends

import logging

from exception import InvalidRequestException, UnsupportedGrantTypeException
from .grants_service import GrantsService
from .client_credentials_service import ClientCredentialsService
from .authorization_code_service import AuthorizationCodeService
from .resource_owner_service import ResourceOwnerService
from .refresh_token_service import RefreshTokenService

from service.client_service import ClientService
from service.user_service import UserService

from models.auth import get_auth_model

logger = logging.getLogger("uvicorn")

'''
grant_type:
    authorization_code:
        in:
            code, redirect_uri
        header:
            authorization: basic 'client_id:secret'

    client_credentials:
        in:
            scope
        header:
            authorization: basic 'client_id:secret'

    password:
        in:
            username, password, scope
        header:
            authorization: basic 'client_id:secret'

    refresh_token
        in:
            rehresh_token
        header:
            authorization: basic 'client_id:secret'
'''

def ServiceFactory(
    grant_type: Optional[str] = Form(None),
    code: Optional[str] = Form(None),
    redirect_uri: Optional[str] = Form(None),
    refresh_token: Optional[str] = Form(None),
    scope: Optional[str] = Form(None),
    client: ClientService = Depends(ClientService),
    user: UserService = Depends(UserService),
    auth_model: dict = Depends(get_auth_model),
):
    if not grant_type:
        raise InvalidRequestException("grant_type not found.")

    client.verify()

    if grant_type == "authorization_code":
        serv = AuthorizationCodeService(client.client_id, code)
    elif grant_type == "password":
        user.verify()
        serv = ResourceOwnerService(client.client_id, user.username, scope)
    elif grant_type == "refresh_token":
        serv = RefreshTokenService(client.client_id, refresh_token)
    elif grant_type == "client_credentials":
        serv = ClientCredentialsService(client.client_id, scope)
    else:
        raise UnsupportedGrantTypeException()

    serv.setModel(auth_model)

    return serv
