
class AuthException(Exception):
    status_code = 400
    error = None
    description = None

    def __init__(self, description = ""):
        self.description = description

    def getStatusCode(self):
        return self.status_code

    def getError(self):
        return self.error

    def getDescription(self):
        return self.description

class InvalidRequestException(AuthException):
    error = "invalid_request"

class InvalidClientException(AuthException):
    status_code = 401
    error = "invalid_client"

class InvalidGrantException(AuthException):
    error = "invalid_grant"

class UnauthorizedClientException(AuthException):
    error = "unauthorized_client"

class UnsupportedGrantTypeException(AuthException):
    error = "unsupported_grant_type"

class InvalidScopeException(AuthException):
    error = "invalid_scope"

# Org
class InvalidUserException(AuthException):
    error = "invalid_user"

class TokenExpiredException(AuthException):
    error = "token_expired"
