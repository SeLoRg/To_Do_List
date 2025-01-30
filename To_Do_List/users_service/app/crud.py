from .schemas import (
    UsersCreateSchema,
    UserGetSchema,
    UsersUpdateSchema,
)
from ..Core.Models import UsersOrm
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import NoResultFound
from sqlalchemy import select, Result
from fastapi import HTTPException
import bcrypt
from fastapi import status, Depends
from .logger import logger


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
        logger.info(f"User founded: id={user.id}")
        return user
    except NoResultFound as e:
        if user_email is not None:
            logger.info(f"User with this email: {user_email} not founded")
        else:
            logger.info(f"User with this id: {user_id} not founded")

        return None


async def create_user(
    session: AsyncSession,
    user_in: UsersCreateSchema,
) -> dict:

    user: UsersOrm | None = await get_user(user_email=user_in.email, session=session)

    if user is not None:
        logger.info(f"User with this email: {user_in.email} already exist")
        return {"detial": f"User with this email: {user_in.email} already exist"}

    try:
        salt = bcrypt.gensalt(rounds=8)
        hash_pwd = bcrypt.hashpw(password=user_in.password.encode(), salt=salt)

        user_create: UsersOrm = UsersOrm(
            password=hash_pwd,
            email=user_in.email,
            username=user_in.username,
            is_active=False,
        )
        session.add(user_create)
        await session.commit()
        logger.info(f"User {user_in.username} created")
        return {"detail": f"User {user_in.username} created"}

    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Invalid server error",
        )


async def update_partial_user(
    user_id: int,
    user_in: UsersUpdateSchema,
    session: AsyncSession,
):
    user: UsersOrm | None = await get_user(user_id=user_id, session=session)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User with this email doesn't exist",
        )

    logger.info(f"User before update: {repr(user)}")
    for k, v in user_in.model_dump(exclude_none=True).items():
        if k == "password":
            salt = bcrypt.gensalt(rounds=10)
            hash_pwd = bcrypt.hashpw(password=v.encode(), salt=salt)

            setattr(user, k, hash_pwd)
        else:
            setattr(user, k, v)

    logger.info(f"User after update: {repr(user)}")
    await session.commit()


async def delete_user(
    user_id: int,
    session: AsyncSession,
) -> None:
    user: UsersOrm | None = await get_user(user_id=user_id, session=session)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with this id={user_id} doesn't exist",
        )

    await session.delete(user)
    await session.commit()
    logger.info(f"User with id={user_id} deleted")
