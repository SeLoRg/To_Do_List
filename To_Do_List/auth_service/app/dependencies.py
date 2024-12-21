import bcrypt
from fastapi import HTTPException, status, Depends

import jwt
import datetime
from ...Core.config.config import settings
import asyncio


async def create_jwt_token(
    user_id: int,
    refresh_id: int,
    typ: str = "access",
):
    if typ == "access":
        payload: dict = {
            "user_id": user_id,
            "typ": typ,
            "refresh_id": refresh_id,
            "iat": datetime.datetime.now(tz=datetime.timezone.utc).timestamp(),
            "exp": (
                datetime.datetime.now(tz=datetime.timezone.utc)
                + settings.token_access_live
            ).timestamp(),
        }
    else:
        payload: dict = {
            "user_id": user_id,
            "typ": typ,
            "refresh_id": refresh_id,
            "iat": datetime.datetime.now(tz=datetime.timezone.utc).timestamp(),
            "exp": (
                datetime.datetime.now(tz=datetime.timezone.utc)
                + settings.token_refresh_live
            ).timestamp(),
        }
    private_key = settings.private_key.read_text()

    return jwt.encode(
        payload=payload,
        key=private_key,
        algorithm=settings.algorithm,
    )
