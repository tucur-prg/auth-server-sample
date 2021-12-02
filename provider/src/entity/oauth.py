from pydantic import BaseModel, Field, validator
from typing import Optional
import logging
import time

from util.id_gen import random_string
import util.pkce as pkce

logger = logging.getLogger("uvicorn")

def code_generator():
    return random_string(5)

def token_generator():
    return random_string(10)

class Code(BaseModel):
    key: str = Field(default_factory=code_generator)
    client_id: str
    username: str
    scope: str
    nonce: str = None
    code_challenge: str = None
    code_challenge_method: str = None
    expire_in: int = 600
    stamp: float = Field(default_factory=time.time)

    def equals(cls, v):
        return cls.client_id == v

    def isExpired(cls):
        now = time.time()
        return (now - cls.stamp) > cls.expire_in

    def validatePKCE(cls, v):
        if not cls.code_challenge_method:
            return True
        elif cls.code_challenge_method.lower() == pkce.PLAIN:
            return cls.code_challenge == v
        return cls.code_challenge == pkce.s256(v.encode())

class Token(BaseModel):
    key: str = Field(default_factory=token_generator)
    client_id: str
    username: str = None
    scope: str = None
    expire_in: int = 3600
    stamp: float = Field(default_factory=time.time)

    def equals(cls, v):
        return cls.client_id == v

    def isExpired(cls):
        now = time.time()
        return (now - cls.stamp) > cls.expire_in

class RefreshToken(Token):
    pass
