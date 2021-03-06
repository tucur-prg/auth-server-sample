from typing import Optional
import logging

from fastapi import Form, Depends

from exception import InvalidUserException

from models.user import get_user_model

logger = logging.getLogger("uvicorn")

class UserService:
    def __init__(
        self,
        username: Optional[str] = Form(""),
        password: Optional[str] = Form(None),   
        model: dict = Depends(get_user_model)
    ):
        self.username = username
        self.password = password
        self.model = model

    def verify(self):
        user = self.model.readUser(self.username)
        if not user:
            raise InvalidUserException()

        if not user.equals(self.password):
            raise InvalidUserException()

        return True
