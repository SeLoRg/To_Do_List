from .schemas import (
    UsersCreateSchema,
    UsersUpdateSchema,
)
from To_Do_List.Models import UsersOrm
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, Result
from sqlalchemy.orm import joinedload
from fastapi import HTTPException
import bcrypt
from fastapi import status
import asyncio


async def create_user(
    session: AsyncSession,
    user_in: UsersCreateSchema,
) -> UsersOrm:

    stmt = select(UsersOrm).where(UsersOrm.email == user_in.email)
    res: Result = await session.execute(stmt)

    if res.scalars().first():
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with this email already registrate",
        )

    if len(user_in.password) < 8:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Invalid password. The password len must be 8 symbols",
        )

    try:
        salt = bcrypt.gensalt()
        hash_pwd = bcrypt.hashpw(password=user_in.password.encode(), salt=salt)

        user_create: UsersOrm = UsersOrm(
            password=hash_pwd,
            email=user_in.email,
            username=user_in.username,
            is_active=False,
        )
        session.add(user_create)
        await session.commit()
        await session.refresh(user_create)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Invalid server error",
        )

    return user_create


async def update_partial_user(
    email: str,
    user_in: UsersUpdateSchema,
    session: AsyncSession,
) -> UsersOrm:
    stmt = select(UsersOrm).where(UsersOrm.email == email)
    res: Result = await session.execute(stmt)
    user: UsersOrm | None = res.scalars().first()

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User with this email doesn't exist",
        )

    for k, v in user_in.model_dump(exclude_none=True).items():
        if k == "password":

            if len(v) < 8:
                raise HTTPException(
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    detail="Invalid password. The password len must be 8 symbols",
                )

            salt = bcrypt.gensalt(rounds=10)
            hash_pwd = bcrypt.hashpw(password=v.encode(), salt=salt)

            setattr(user, k, hash_pwd)
        else:
            setattr(user, k, v)

    await session.commit()

    return user
