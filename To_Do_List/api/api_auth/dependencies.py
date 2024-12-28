import bcrypt
from fastapi import HTTPException, status, Depends

import jwt
import datetime


from sqlalchemy import Result, select
from sqlalchemy.ext.asyncio import AsyncSession

from To_Do_List.Core.config.config import settings
from fastapi_mail import FastMail, MessageSchema
import asyncio

from To_Do_List.Core.Database.database import database
from To_Do_List.Core.Models import UsersOrm
from To_Do_List.api.api_auth.shemas import UserLogin


async def create_jwt_token(
    user_email: str,
    user_id: int,
    typ: str = "access",
):
    if typ == "access":
        payload: dict = {
            "sub": user_id,
            "typ": typ,
            "email": user_email,
            "iat": datetime.datetime.now(tz=datetime.timezone.utc).timestamp(),
            "exp": (
                datetime.datetime.now(tz=datetime.timezone.utc)
                + settings.auth_jwt.token_access_live
            ).timestamp(),
        }
    else:
        payload: dict = {
            "sub": user_id,
            "typ": typ,
            "iat": datetime.datetime.now(tz=datetime.timezone.utc).timestamp(),
            "exp": (
                datetime.datetime.now(tz=datetime.timezone.utc)
                + settings.auth_jwt.token_refresh_live
            ).timestamp(),
        }

    private_key = await asyncio.to_thread(settings.auth_jwt.private_key.read_text)

    return jwt.encode(
        payload=payload,
        key=private_key,
        algorithm=settings.auth_jwt.algorithm,
    )
