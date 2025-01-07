from sqlalchemy.ext.asyncio import AsyncSession
from ..Core.Models import UsersOrm
from sqlalchemy import select, Result
from .logger import logger
from sqlalchemy.exc import NoResultFound
from fastapi import HTTPException, status


async def get_user(
    session: AsyncSession,
    user_id: int | None = None,
    user_email: str | None = None,
) -> UsersOrm | None:
    if user_email is not None:
        stmt = select(UsersOrm).where(UsersOrm.email == user_email)
    else:
        stmt = select(UsersOrm).where(UsersOrm.id == user_id)
    res: Result = await session.execute(stmt)
    try:
        user: UsersOrm = res.scalars().one()
        return user
    except NoResultFound as e:
        if user_email is not None:
            logger.info(f"User with this email: {user_email} not founded")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with this email: {user_email} not founded",
            )
        else:
            logger.info(f"User with this id: {user_id} not founded")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with this id: {user_id} not founded",
            )
