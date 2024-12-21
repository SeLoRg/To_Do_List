from .shemas import UserLoginSchema
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Response, HTTPException, status
import bcrypt
import asyncio
import datetime
from ...Core.config.config import settings
from . import dependencies
from sqlalchemy import select, Result
from sqlalchemy.exc import NoResultFound
from ...Core.Models import UsersOrm, RefreshListOrm, RefreshBlackListOrm


async def login_user(
    data: UserLoginSchema, session: AsyncSession, response: Response
) -> dict[str, str]:
    stmt = select(UsersOrm).where(UsersOrm.email == data.email)
    res: Result = await session.execute(stmt)
    try:
        user: UsersOrm = res.scalars().one()
        # await session.refresh(user)
    except NoResultFound:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password"
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Email not confirmed"
        )

    if not bcrypt.checkpw(
        password=data.password.encode(), hashed_password=user.password
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid password"
        )
    refresh_list = RefreshListOrm(
        user_id=user.id,
        expire=(
            datetime.datetime.now(tz=datetime.timezone.utc) + settings.token_access_live
        ).timestamp(),
    )

    print(f"User id : {user.id}")
    session.add(refresh_list)
    await session.commit()
    await session.refresh(refresh_list)

    stmt = select(RefreshBlackListOrm).where(
        RefreshBlackListOrm.refresh_id == refresh_list.id
    )
    res: Result = await session.execute(stmt)
    # await session.commit()
    if res.scalars().first() is not None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token"
        )
    # refresh_id: int = refresh_list.id
    # user_id: int = user.id
    # print(user_id)
    # print(f"Refresh token created : {refresh_id}")
    token_refresh, token_access = await asyncio.gather(
        dependencies.create_jwt_token(
            refresh_id=refresh_list.id,
            user_id=1,
            typ="refresh",
        ),
        dependencies.create_jwt_token(
            refresh_id=1,
            user_id=2,
        ),
    )

    response.set_cookie(
        key=settings.COOKIE_JWT_REFRESH,
        value=token_refresh,
        max_age=2592000,
        httponly=True,
        secure=True,
        samesite="lax",
    )
    response.set_cookie(
        key=settings.COOKIE_JWT_ACCESS,
        value=token_access,
        max_age=900,
        httponly=True,
        secure=True,
        samesite="lax",
    )

    return {"detail": f"user: {data.email} login successfully"}
