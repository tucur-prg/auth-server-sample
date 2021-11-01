import logging
import time

from util.id_gen import random_string

logger = logging.getLogger("uvicorn")

class Code:
    def __init__(self, *args, client_id, username, scope, expire_in = 600, **keys):
        self.client_id = client_id
        self.username = username
        self.scope = scope
        self.expire_in = expire_in
        self.key = keys["key"] if "key" in keys else self._generateKey()
        self.stamp = keys["stamp"] if "stamp" in keys else time.time()

    def _generateKey(self):
        return random_string(5)
        
    def equals(self, client_id):
        return self.client_id == client_id

    def isExpired(self):
        now = time.time()
        return (now - self.stamp) > self.expire_in

class Token:
    def __init__(self, *args, client_id, username = None, scope = None, expire_in = 3600, key = None, stamp = None, **keys):
        self.client_id = client_id
        self.username  = username
        self.scope     = scope
        self.expire_in = expire_in
        self.key       = key if key else self._generateKey()
        self.stamp     = stamp if stamp else time.time()

    def _generateKey(self):
        return random_string(10)

    def equals(self, client_id):
        return self.client_id == client_id

    def isExpired(self):
        now = time.time()
        return (now - self.stamp) > self.expire_in

class RefreshToken(Token):
    pass
