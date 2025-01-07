import asyncio
import datetime
from ..Core.config.config import settings
from sqlalchemy import select, Result
from ..Core.Models import UsersOrm, SessionsOrm
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import NoResultFound
from fastapi import Response, HTTPException, status
import jwt
from .logger import logger


async def create_jwt_token(
    user_id: int,
    session_id: int,
    typ: str = "access",
) -> str:
    if typ == "access":
        payload: dict = {
            "user_id": user_id,
            "typ": typ,
            "session_id": session_id,
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
            "session_id": session_id,
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


async def create_user_session(session: AsyncSession, user_id: int) -> int:
    user_session = SessionsOrm(user_id=user_id)
    session.add(user_session)
    await session.flush()
    await session.refresh(user_session)
    return user_session.id


async def check_user_session(session: AsyncSession, user_id: int) -> int | None:
    stmt = select(SessionsOrm).where(SessionsOrm.user_id == user_id)
    res: Result = await session.execute(stmt)
    try:
        user_session: SessionsOrm = res.scalars().one()
        return user_session.id
    except NoResultFound as e:
        logger.info(f"Session for user {user_id} not founded")
        return None


# async def reissue_token(session: AsyncSession, access_token: str) -> str:
#     try:
#         payload: dict = jwt.decode(
#             jwt=access_token,
#             key=settings.publik_key.read_text(),
#             algorithms=settings.algorithm,
#             options={"verify_exp": False},
#         )
#     except jwt.InvalidTokenError as e:
#
#
#     stmt = select(RefreshBlackListOrm).where(
#         RefreshBlackListOrm.refresh_id == payload.get("refresh_id")
#     )
#     res: Result = await session.execute(stmt)
#     if res.scalars().first() is not None:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
#         )
#
#     access_token = await dependencies.create_jwt_token(
#         user_id=payload.get("user_id"), refresh_id=payload.get("refresh_id")
#     )
#     return access_token
