from pydantic import BaseModel, Field, validator
from typing import Optional
import logging
import time

from util.id_gen import random_string

logger = logging.getLogger("uvicorn")

def password_generator():
    return "secret987"

TYPE_PUBLIC = "public"
TYPE_CONFIDENTIAL = "confidential"

class Client(BaseModel):
    client_id: str
    client_secret: str = Field(default_factory=password_generator)
    name: str
    type: Optional[str] = TYPE_PUBLIC
    redirect_uri: Optional[str] = None
    create_at: float = Field(default_factory=time.time)

    @validator("type")
    def type_match(cls, v):
        if v.lower() == TYPE_PUBLIC or v.lower() == TYPE_CONFIDENTIAL:
            return v
        raise ValueError(f"type \"{v}\" is no match.")

    def equals(cls, v):
        return cls.client_secret == v
