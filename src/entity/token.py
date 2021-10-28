import logging
import time

from util.id_gen import random_string

logger = logging.getLogger("uvicorn")

class Token:
    def __init__(self, *args, client_id, username = None, scope = None, expire_in = 3600, key = None, stamp = None, **keys):
        self.client_id = client_id
        self.username  = username
        self.scope     = scope
        self.expire_in = expire_in
        self.key       = key if key else self._generateToken()
        self.stamp     = stamp if stamp else time.time()

    def _generateToken(self):
        return random_string(10)

class RefreshToken(Token):
    pass
