import asyncio
import datetime
from ...Core.config.config import settings
from . import dependencies
from sqlalchemy import select, Result
from ...Core.Models import UsersOrm, RefreshListOrm, RefreshBlackListOrm
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Response, HTTPException, status
import jwt


async def issue_tokens(session: AsyncSession, user_id: int, response: Response) -> None:
    refresh_list = RefreshListOrm(
        user_id=user_id,
        expire=(
            datetime.datetime.now(tz=datetime.timezone.utc) + settings.token_access_live
        ).timestamp(),
    )

    session.add(refresh_list)
    await session.flush()

    token_refresh, token_access = await asyncio.gather(
        dependencies.create_jwt_token(
            refresh_id=refresh_list.id,
            user_id=user_id,
            typ="refresh",
        ),
        dependencies.create_jwt_token(
            refresh_id=refresh_list.id,
            user_id=user_id,
        ),
    )

    response.set_cookie(
        key=settings.COOKIE_JWT_REFRESH,
        value=token_refresh,
        max_age=2678400,
        httponly=True,
        secure=True,
        samesite="lax",
    )
    response.set_cookie(
        key=settings.COOKIE_JWT_ACCESS,
        value=token_access,
        max_age=87300,
        httponly=True,
        secure=True,
        samesite="lax",
    )


async def check_blacklist_refresh_jwt(session: AsyncSession, refresh_id: int) -> bool:
    stmt = select(RefreshBlackListOrm).where(
        RefreshBlackListOrm.refresh_id == refresh_id
    )


async def reissue_token(session: AsyncSession, access_token: str) -> str:
    payload: dict = jwt.decode(
        jwt=access_token,
        key=settings.publik_key.read_text(),
        algorithms=settings.algorithm,
        options={"verify_exp": False},
    )

    stmt = select(RefreshBlackListOrm).where(
        RefreshBlackListOrm.refresh_id == payload.get("refresh_id")
    )
    res: Result = await session.execute(stmt)
    if res.scalars().first() is not None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
        )

    access_token = await dependencies.create_jwt_token(
        user_id=payload.get("user_id"), refresh_id=payload.get("refresh_id")
    )
    return access_token
