from typing import Optional

from fastapi import Form, Depends

import logging

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
        user = self.model.getUser(self.username)
        if not user:
            raise InvalidUserException()

        if user["password"] != self.password:
            raise InvalidUserException()

        return True
