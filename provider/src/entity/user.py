from pydantic import BaseModel, Field, validator
from typing import Optional
import logging
import time

from util.id_gen import random_string

logger = logging.getLogger("uvicorn")

def password_generator():
    return "Passw0rd"

class User(BaseModel):
    username: str
    password: str = Field(default_factory=password_generator)
    create_at: float = Field(default_factory=time.time)

    def equals(cls, v):
        return cls.password == v
