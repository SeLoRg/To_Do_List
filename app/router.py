import uuid

from fastapi import APIRouter, Depends, HTTPException, status, Response, Header, Cookie
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from typing import Annotated, Any
from fastapi_users.authentication import CookieTransport
import secrets

router = APIRouter()
security = HTTPBasic()
cookie_transport = CookieTransport(cookie_max_age=3600)

fake_users = {
    "admin": "admin",
    "selorg": "1234",
}

fake_tokens = {
    "jdjfhdg33jnfiue": "admin",
    "jnjbyybjnkuigusknfo": "selorg",
}

COOKIES: dict[str, dict[str, Any]] = {}


async def token_auth_username(
    token: str = Header(alias="auth-token"),
):
    auth_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid token",
    )

    if username := fake_tokens.get(token):
        return username

    raise auth_exception


@router.get("/basi-auth/")
async def token_auth(username: str = Depends(token_auth_username)):
    return {"message": f"Hi, {username}!", "username": username}


@router.post("/cookie-login/")
async def cookie_login(
    response: Response,
    username: str = Depends(token_auth_username),
):
    session_id = uuid.uuid4().hex
    COOKIES[session_id] = {
        "username": username,
    }
    response.set_cookie("cookie", session_id)
    return {"message": "ok"}


@router.get("/check-cookie/")
async def check_cookie(session_id: str = Cookie(alias="cookie")):
    if session_id not in COOKIES:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="not authenticated"
        )

    return {"username": COOKIES[session_id]["username"]}
