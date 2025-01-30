import json

from sqlalchemy.ext.asyncio import AsyncSession
from Core.Models import UsersOrm, SessionsOrm
from sqlalchemy import select, Result, or_
from .logger import logger
from sqlalchemy.exc import NoResultFound
from fastapi import HTTPException, status
from Core.redis_client.redis_client import redis_client
from Core.config import settings


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


async def create_user_session(session: AsyncSession, user_id: int) -> SessionsOrm:
    user_session = SessionsOrm(user_id=user_id)
    session.add(user_session)
    await session.flush()
    await session.refresh(user_session)
    return user_session


async def get_user_session(
    session: AsyncSession,
    user_id: int | None = None,
    session_id: int | None = None,
) -> SessionsOrm | None:

    stmt = select(SessionsOrm).where(
        or_(
            SessionsOrm.user_id == user_id,
            SessionsOrm.id == session_id,
        )
    )
    res: Result = await session.execute(stmt)
    try:
        user_session = res.scalars().one()
        return user_session
    except NoResultFound as e:
        logger.info(f"Session not founded")
        return None
