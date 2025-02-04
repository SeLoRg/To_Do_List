import json

import jwt

from .shemas import (
    UserLoginSchema,
    Credentials,
    UserRegistrateSchema,
    CheckAuthResponse,
    UserLoginResponse,
    CheckAuthRequest,
    LogoutRequest,
    Tokens,
)
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Response, HTTPException, status, Depends, Request
from pydantic import BaseModel
from .logger import logger
import httpx
from typing import Dict, Any
from Core.Models import UsersOrm, SessionsOrm
from . import crud
import bcrypt
from Core.config import settings
from datetime import timedelta, datetime, timezone
from Core.redis_client.redis_client import redis_client
import asyncio
from grpc import RpcError


async def create_jwt_token(
    **kwargs,
) -> str:
    payload: dict = {
        **kwargs,
        "iat": datetime.now(tz=timezone.utc).timestamp(),
        "exp": (datetime.now(tz=timezone.utc) + settings.token_access_live).timestamp(),
    }
    private_key = settings.private_key.read_text()

    return jwt.encode(
        payload=payload,
        key=private_key,
        algorithm=settings.algorithm,
    )


async def login(
    data: UserLoginSchema,
    session_user: AsyncSession,
    session_sessions: AsyncSession,
) -> UserLoginResponse | HTTPException:
    try:
        logger.info(f"Try find user with email={data.email} in db")
        user: UsersOrm | None = await crud.get_user(
            user_email=data.email, session=session_user
        )

        if user is None:
            logger.info(f"User {data.email} not founded")
            return HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User {data.email} not founded",
            )

        logger.info(f"User founded: id={user.id}")

        logger.info("Check password")
        if not bcrypt.checkpw(
            password=data.password.encode(), hashed_password=user.password
        ):
            return HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="invalid password",
            )

        logger.info(f"Try find user_session in db")
        user_session: SessionsOrm | None = await crud.get_user_session(
            session=session_sessions,
            user_id=user.id,
        )

        if user_session is None:
            logger.info("Create session")
            user_session = await crud.create_user_session(
                user_id=user.id,
                agent=data.agent,
                ip=data.ip,
                session=session_sessions,
            )
            logger.info(f"Session created")

        logger.info(f"user session:id={user_session.id}")
        logger.info(f"Set session in cache")
        logger.info(f"Create access token")

        res: tuple = await asyncio.gather(
            redis_client.set(
                name=user_session.refresh_token,
                value=json.dumps(
                    {
                        "user_id": user_session.user_id,
                        "id": user_session.id,
                        "agent": user_session.agent,
                        "ip": user_session.ip,
                        "is_valid": user_session.is_valid,
                        "expire": user_session.expire,
                    }
                ).encode(),
                ex=timedelta(hours=1),
            ),
            create_jwt_token(user_id=user.id, user_email=user.email),
        )

        access_token: str = res[1]
        refresh_token: str = user_session.refresh_token
        await session_sessions.commit()
        await session_user.close()
        logger.info(
            f"Access token created: {access_token}, Refresh token: {refresh_token}"
        )
        return UserLoginResponse(
            is_login=True, access_token=access_token, refresh_token=refresh_token
        )

    except HTTPException as e:
        return HTTPException(status_code=e.status_code, detail=f"{e}")

    except Exception as e:
        return HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"{e}"
        )


async def logout(
    credentials: LogoutRequest,
    session_sessions: AsyncSession,
) -> HTTPException | None:
    try:
        logger.info(f"Try get user session form db")
        user_session: None | SessionsOrm = await crud.get_user_session(
            session=session_sessions, user_id=credentials.user_id
        )

        if user_session is not None:
            logger.info(f"Try delete user session")
            await session_sessions.delete(user_session)
            await session_sessions.commit()

            logger.info(f"Try to get user_session from cache")
            redis_key_session: str = f"{user_session.refresh_token}"
            user_session = await redis_client.get(name=redis_key_session)

            if user_session is not None:
                logger.info(f"del user session from cache")
                await redis_client.delete(redis_key_session)

            return

        logger.info(f"user_session in db not founded")
        return
    except Exception as e:
        return HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


async def check_authenticate(
    data: CheckAuthRequest,
    session_sessions: AsyncSession,
) -> CheckAuthResponse:
    response: CheckAuthResponse = CheckAuthResponse()

    try:
        if data.access_token is None or data.refresh_token is None:
            response.is_login = False
            return response

        payload: dict = jwt.decode(
            jwt=data.access_token,
            key=settings.public_key.read_text(),
            algorithms=settings.algorithm,
            options={"verify_exp": False},
        )
        # Истек ли токен?
        if payload.get("exp") < datetime.now(tz=timezone.utc).timestamp():
            logger.info(f"access token expired")

            logger.info(f"get user session from db")
            user_session: SessionsOrm | None = await crud.get_user_session(
                session=session_sessions,
                token=data.refresh_token,
            )

            if user_session is None:
                logger.info("user is not authenticated")
                return response

            if data.ip != user_session.ip or data.agent != user_session.agent:
                logger.info("user is not authenticated")
                return response

            if datetime.now(tz=timezone.utc).timestamp() >= user_session.expire:
                logger.info("user is not authenticated")
                await session_sessions.delete(user_session)
                await session_sessions.commit()
                return response

            new_user_session: SessionsOrm = await crud.create_user_session(
                session=session_sessions,
                user_id=user_session.user_id,
                agent=user_session.agent,
                ip=user_session.ip,
            )
            await session_sessions.delete(user_session)
            new_access_token: str = await create_jwt_token(**payload)
            new_refresh_token: str = new_user_session.refresh_token
            logger.info(
                f"new tokens:\naccess={new_access_token}\nrefresh={new_refresh_token}"
            )
            response.new_tokens = Tokens(
                access_token=new_access_token, refresh_token=new_refresh_token
            )
            await session_sessions.commit()

        response.is_login = True
        response.credentials = Credentials(**payload)

        return response

    except jwt.InvalidTokenError as e:
        logger.error(f"Invalid token: {e}")
        return response
    except Exception as e:
        logger.error(f"Error when decode jwt: {e}")
        return response
