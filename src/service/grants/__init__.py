from typing import Optional
import logging

from fastapi import Form, Depends

from exception import UnsupportedGrantTypeException

from .grants_service import GrantsService
from .client_credentials_service import ClientCredentialsService
from .authorization_code_service import AuthorizationCodeService
from .resource_owner_service import ResourceOwnerService
from .refresh_token_service import RefreshTokenService

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
    authz: AuthorizationCodeService = Depends(AuthorizationCodeService),
    rop: ResourceOwnerService = Depends(ResourceOwnerService),
    token: RefreshTokenService = Depends(RefreshTokenService),
    cc: ClientCredentialsService = Depends(ClientCredentialsService),
):

    if grant_type == "authorization_code":
        return authz
    elif grant_type == "password":
        return rop
    elif grant_type == "refresh_token":
        return token
    elif grant_type == "client_credentials":
        return cc

    raise UnsupportedGrantTypeException()
