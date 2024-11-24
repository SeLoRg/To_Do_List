import bcrypt
from fastapi import HTTPException, Cookie, status, Depends

import jwt
import datetime


from sqlalchemy import Result, select
from sqlalchemy.ext.asyncio import AsyncSession

from To_Do_List.Core.config import settings
from fastapi_mail import FastMail, MessageSchema
import asyncio

from To_Do_List.Core.database import database
from To_Do_List.Models import UsersOrm
from To_Do_List.api.api_auth.shemas import UserLogin


async def send_email_task(fm: FastMail, message: MessageSchema):
    await fm.send_message(message)


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


async def create_temp_jwt_token(email: str, session: AsyncSession):
    stmt = select(UsersOrm).where(UsersOrm.email == email)
    res: Result = await session.execute(stmt)
    user: UsersOrm = res.scalars().first()

    return await create_jwt_token(user_email=user.email, user_id=user.id)


async def validate_user(
    data: UserLogin,
    session: AsyncSession = Depends(database.get_session),
) -> UsersOrm:
    stmt = select(UsersOrm).where(UsersOrm.email == data.email)
    res: Result = await session.execute(stmt)
    user: UsersOrm | None = res.scalars().first()

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Invalid email"
        )

    if not bcrypt.checkpw(
        password=data.password.encode(), hashed_password=user.password
    ):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Invalid password"
        )

    return user
