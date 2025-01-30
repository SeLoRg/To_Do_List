import json

import jwt

from .shemas import (
    UserLoginSchema,
    RequestCredentials,
    UserRegistrateSchema,
    ResponseCredentials,
    CheckAuthResponse,
    UserLoginResponse,
    LogoutRequest,
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
    typ: str = "access",
    **kwargs,
) -> str:
    if typ == "access":
        payload: dict = {
            **kwargs,
            "typ": typ,
            "iat": datetime.now(tz=timezone.utc).timestamp(),
            "exp": (
                datetime.now(tz=timezone.utc) + settings.token_access_live
            ).timestamp(),
        }
        # logger.info(f"payload={payload}")
    else:
        payload: dict = {
            **kwargs,
            "typ": typ,
            "iat": datetime.now(tz=timezone.utc).timestamp(),
            "exp": (
                datetime.now(tz=timezone.utc) + settings.token_refresh_live
            ).timestamp(),
        }
    private_key = settings.private_key.read_text()

    return jwt.encode(
        payload=payload,
        key=private_key,
        algorithm=settings.algorithm,
    )


async def get_credentials_from_jwt(token: str) -> ResponseCredentials | None:
    try:
        payload: dict = jwt.decode(
            jwt=token,
            key=settings.public_key.read_text(),
            algorithms=settings.algorithm,
        )
        return ResponseCredentials(**payload)
    except jwt.ExpiredSignatureError as e:
        logger.info(f"token expired")
        return None
    except jwt.InvalidTokenError as e:
        logger.error(f"Invalid token: {e}")
        return None
    except Exception as e:
        logger.error(f"Error when decode jwt: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="f{e}"
        )


async def send_request(
    method: str,
    url: str,
    headers: dict | None = None,
    data: dict | BaseModel = None,
    params: dict | None = None,
) -> Response | Any:
    try:
        async with httpx.AsyncClient() as client:
            if isinstance(data, BaseModel):
                data = data.model_dump()

            request = client.build_request(
                method=method, url=url, headers=headers, json=data, params=params
            )
            response = await client.send(request=request)
            response.raise_for_status()
            return Response(response.content, response.status_code, response.headers)
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


async def registrate(
    data: UserRegistrateSchema,
    response: Response,
) -> dict:
    try:
        response_from_users: Response = await send_request(
            method="PUT", url="http://localhost:8001/create-user", data=data
        )

        response = response_from_users
        if 200 <= response.status_code < 300:
            return {"detail": "user create success"}

    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=f"{e.detail}")
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"{e}"
        )


async def login(
    data: UserLoginSchema,
    session_user: AsyncSession,
    session_sessions: AsyncSession,
) -> UserLoginResponse | HTTPException:
    try:
        logger.info(f"try find user with email={data.email} in db")
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
                user_id=user.id, session=session_sessions
            )
            logger.info(f"Session created")

        logger.info(f"user session:id={user_session.id}")
        logger.info(f"Set session in cache")
        logger.info(f"Create access token")

        res: tuple = await asyncio.gather(
            redis_client.set(
                name=f"{settings.KEY_USER_SESSION}{user.email}",
                value=json.dumps(
                    {"user_id": user_session.user_id, "id": user_session.id}
                ).encode(),
                ex=timedelta(hours=1),
            ),
            create_jwt_token(
                user_id=user.id, user_email=user.email, session_id=user_session.id
            ),
        )

        access_token: str = res[1]
        await session_sessions.commit()
        logger.info(f"Access token created: {access_token}")
        return UserLoginResponse(access_token=access_token)

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

        logger.info(f"try get user session form db")
        user_session: None | bytes | SessionsOrm = await crud.get_user_session(
            session=session_sessions, session_id=credentials.session_id
        )

        if user_session is not None:
            logger.info(f"Try delete user session")
            await session_sessions.delete(user_session)
            await session_sessions.commit()

        logger.info(f"user_session not founded")

        logger.info(f"Try to get user_session from cache")
        redis_key_session: str = f"{settings.KEY_USER_SESSION}{credentials.user_email}"
        user_session = await redis_client.get(name=redis_key_session)

        if user_session is not None:
            logger.info(f"del user session from cache")
            await redis_client.delete(redis_key_session)

        return
    except Exception as e:
        return HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


async def check_authenticate(
    access_token: str | None,
    session_sessions: AsyncSession,
) -> CheckAuthResponse | None:
    try:
        if access_token is None:
            return None

        res: CheckAuthResponse = CheckAuthResponse()

        payload: dict = jwt.decode(
            jwt=access_token,
            key=settings.public_key.read_text(),
            algorithms=settings.algorithm,
            options={"verify_exp": False},
        )
        res.credentials = ResponseCredentials(**payload)
        # Истек ли токен?
        if payload.get("exp") < datetime.now(tz=timezone.utc).timestamp():

            logger.info(f"token expired")
            res.token_exp = True
            redis_key = f"{settings.KEY_USER_SESSION}{payload.get("user_email")}"
            logger.info(f"try get user session from cache by key={redis_key}")
            user_session: SessionsOrm | None | bytes = await redis_client.get(redis_key)

            if user_session is not None:
                user_session = SessionsOrm(**json.loads(user_session.decode()))
            else:
                logger.info(f"get user session from db")
                user_session = await crud.get_user_session(
                    session=session_sessions,
                    session_id=payload.get("session_id"),
                )
            if user_session is None:
                logger.info("user session not founded")
                return None

            if user_session.user_id != payload.get("user_id"):
                logger.info("user session not founded")
                return None

            logger.info(f"set user session in cache")
            await redis_client.set(
                name=redis_key,
                value=json.dumps(
                    {"user_id": user_session.user_id, "id": user_session.id}
                ).encode(),
                ex=timedelta(hours=1),
            )

            access_token: str = await create_jwt_token(**payload)
            res.new_token = access_token
            logger.info(f"new token={access_token}")

        return res

    except jwt.InvalidTokenError as e:
        logger.error(f"Invalid token: {e}")
        return None
    except Exception as e:
        logger.error(f"Error when decode jwt: {e}")
        return None
