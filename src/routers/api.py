from typing import Optional
import logging

from fastapi import APIRouter, Header

logger = logging.getLogger("uvicorn")

router = APIRouter()

@router.get("/v1/user", tags=["api"])
async def user(
    authorization: Optional[str] = Header(None),
):
    if not authorization:
        return {
            "error": "access_denied",
        }

    type, token = authorization.split(' ')
    if type.lower() != 'bearer':
        return {
            "error": "access_denied",
        }

    # TODO: tokenの検証 APIとしての共通処理にしたい

    logger.info(type)
    logger.info(token)

    return {
        "user": "test"
    }
