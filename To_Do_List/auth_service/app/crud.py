import json

from sqlalchemy.ext.asyncio import AsyncSession
from Core.Models import UsersOrm, SessionsOrm
from sqlalchemy import select, Result, or_
from .logger import logger
from sqlalchemy.exc import NoResultFound
from fastapi import HTTPException, status
from Core.redis_client.redis_client import redis_client
from Core.config import settings
import datetime

import secrets
import string


def generate_random_token(length=32):
    alphabet = string.ascii_letters + string.digits
    return "".join(secrets.choice(alphabet) for i in range(length))


async def get_user(
    session: AsyncSession,
    user_id: int | None = None,
    user_email: str | None = None,
) -> UsersOrm | None:
    stmt = select(UsersOrm).where(
        or_(UsersOrm.email == user_email, UsersOrm.id == user_id)
    )
    res: Result = await session.execute(stmt)
    try:
        user: UsersOrm = res.scalars().one()
        return user
    except NoResultFound as e:
        if user_email is not None:
            logger.info(f"User with this email: {user_email} not founded")
        else:
            logger.info(f"User with this id: {user_id} not founded")

        return


async def get_user_session(
    session: AsyncSession,
    user_id: int | None = None,
    session_id: int | None = None,
    token: str | None = None,
) -> SessionsOrm | None:

    stmt = select(SessionsOrm).where(
        or_(
            SessionsOrm.user_id == user_id,
            SessionsOrm.id == session_id,
            SessionsOrm.refresh_token == token,
        )
    )
    res: Result = await session.execute(stmt)
    try:
        user_session = res.scalars().one()
        return user_session
    except NoResultFound as e:
        logger.info(f"Session not founded")
        return None


async def create_user_session(
    session: AsyncSession, user_id: int, agent: str, ip: str
) -> SessionsOrm:
    refresh_token: str = generate_random_token()

    user_session: SessionsOrm | None = await get_user_session(
        session=session, token=refresh_token
    )

    while user_session is not None:
        refresh_token = generate_random_token()
        user_session = await get_user_session(session=session, token=refresh_token)

    user_session = SessionsOrm(
        user_id=user_id,
        agent=agent,
        ip=ip,
        refresh_token=refresh_token,
        expire=(
            datetime.datetime.now(tz=datetime.timezone.utc)
            + settings.token_refresh_live
        ).timestamp(),
        is_valid=True,
    )
    session.add(user_session)
    await session.flush()
    await session.refresh(user_session)
    return user_session
