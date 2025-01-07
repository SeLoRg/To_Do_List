from .shemas import UserLoginSchema
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Response, HTTPException, status
from pydantic import BaseModel
from .logger import logger
import httpx
from typing import Dict, Any
from ..Core.Models import UsersOrm
from . import crud
import bcrypt
from . import authentication
from ..Core.config import settings


async def send_request(
    method: str,
    url: str,
    headers: dict | None = None,
    data: dict | BaseModel = None,
    params: dict | None = None,
) -> dict | Any:
    try:
        async with httpx.AsyncClient() as client:
            if isinstance(data, BaseModel):
                data = data.model_dump()

            request = client.build_request(
                method=method, url=url, headers=headers, json=data, params=params
            )
            response = await client.send(request=request)
            response.raise_for_status()
            return response.json()
    except httpx.HTTPError as e:
        logger.error(f"Http error during send {data} to: {url}. Error: {e}")
        raise HTTPException(
            status_code=response.status_code, detail=f"Error during HTTP request: {e}"
        )
    except Exception as e:
        logger.error(f"Error during send message to {url}. Error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error during HTTP request: {e}",
        )


async def login(
    data: UserLoginSchema,
    response: Response,
    session_users: AsyncSession,
    session_sessions: AsyncSession,
) -> None:
    logger.info(f"try find user with email={data.email}")
    user: UsersOrm = await crud.get_user(session=session_users, user_email=data.email)
    logger.info(f"User founded: id={user.id}")

    logger.info("Check password")
    if not bcrypt.checkpw(
        password=data.password.encode(), hashed_password=user.password
    ):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="invalid password"
        )

    logger.info(f"Try find user_session")
    user_session: int | None = await authentication.check_user_session(
        session=session_sessions, user_id=user.id
    )

    if user_session is None:
        logger.info("Create session")
        user_session = await authentication.create_user_session(
            session=session_sessions, user_id=user.id
        )
        logger.info(f"Session created")

    logger.info(f"user session:id={user_session}")
    logger.info(f"Create access token")
    access_token: str = await authentication.create_jwt_token(
        user_id=user.id, session_id=user_session
    )
    logger.info(f"Access token created: {access_token}")

    response.set_cookie(
        key=settings.COOKIE_JWT_ACCESS,
        value=access_token,
        max_age=87300,
        httponly=True,
        secure=True,
        samesite="lax",
    )

    await session_sessions.commit()
