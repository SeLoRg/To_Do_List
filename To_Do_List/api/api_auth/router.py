from fastapi import (
    Response,
    Cookie,
    APIRouter,
    BackgroundTasks,
    status,
    Depends,
    HTTPException,
    Header,
)
from fastapi_mail import FastMail, MessageSchema


from To_Do_List.Core.config import settings
from To_Do_List.api.api_auth import dependencies
from .shemas import EmailVerificationRequest, UserLogin
from sqlalchemy.ext.asyncio import AsyncSession
from To_Do_List.Core.database import database
import jwt
from sqlalchemy import select, Result
from To_Do_List.Models import UsersOrm
import os
import aiofiles
import bcrypt


router = APIRouter(tags=["Auth"], prefix="/auth")
COOKIE_JWT_REFRESH: str = "jwt-refresh-token"
COOKIE_JWT_ACCESS: str = "jwt-access-token"


@router.post("/set-cookie-token/", status_code=status.HTTP_200_OK)
async def set_token_cookie(response: Response, value: str | None = None):
    # response.delete_cookie(
    #     key="eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOjcxLCJ0eXAiOiJhY2Nlc3MiLCJlbWFpbCI6InJvc3Rpc2xhdm1hcmlub3ZAYmsucnUiLCJpYXQiOjE3MzE3ODUwNDEuOTAzNjg2LCJleHAiOjE3MzE3ODUxMDEuOTAzNjg2fQ.C9AJ0jb49YG2HF1HGp4Ck9vuPtM2cNZr8r2QnM1FBPxIHxwMM12auV2jQ7CQeh7QgCDJBM5W6acxxOm2rXF5K4z81S-OaoBN35WfVnb6eXkRz87WLaCgM2w1fG7Ka0WCZvfIsJcV4bPHxcdXskwijNnJBrQLg9okI3sstXXb9WkbXtYmFRfxjhLt4jJ82nJ__HpQY-w9Cbzn_w80A7te23pkrp9avNKznp-NDSVBYZIYOBM7loV7XCVMy_kpa6oiNXUzbxdYi4Y5DNxps8tHtK7y275cftj1jxmfZrIvFRhAI8MDYElig2paO1kISNb2velgYl2Xllfb92qmhirw-w"
    # )
    # response.delete_cookie(key=COOKIE_JWT_REFRESH)
    response.set_cookie(key=COOKIE_JWT_ACCESS, value=value, max_age=5555555)
    return {"message": "Cookie successfully set"}


@router.post("/login", status_code=status.HTTP_200_OK)
async def login(
    response: Response,
    user: UsersOrm = Depends(dependencies.validate_user),
):
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Email not confirmed"
        )

    token_refresh = await dependencies.create_jwt_token(
        user_email=user.email,
        user_id=user.id,
        typ="refresh",
    )
    token_access = await dependencies.create_jwt_token(
        user_email=user.email,
        user_id=user.id,
    )
    response.set_cookie(key=COOKIE_JWT_REFRESH, value=token_refresh, max_age=604800)
    response.set_cookie(key=COOKIE_JWT_ACCESS, value=token_access, max_age=604800)

    response.headers["Authorization"] = f"Bearer {token_access}"

    return {"detail": "user login"}


@router.post("/send-email-update-password", status_code=status.HTTP_200_OK)
async def update_password(
    request: EmailVerificationRequest,
    background_tasks: BackgroundTasks,
):
    html_path = os.path.join("To_Do_List/api/api_auth/html", "update-password.html")
    async with aiofiles.open(html_path, "r", encoding="utf-8") as file:
        html_content = await file.read()
    html_content = html_content.replace("{{email}}", request.email)
    email_message: MessageSchema = MessageSchema(
        subject="Обновление пароля",
        recipients=[request.email],
        body=html_content,
        subtype="html",
    )

    fm = FastMail(config=settings.smtp_conf)
    background_tasks.add_task(dependencies.send_email_task, fm, email_message)

    return {"detail": "email send"}


@router.post("/send-email-verification", status_code=status.HTTP_200_OK)
async def send_email_verification(
    request: EmailVerificationRequest,
    background_tasks: BackgroundTasks,
    session: AsyncSession = Depends(database.get_session),
):
    html_path = os.path.join("To_Do_List/api/api_auth/html", "email_verification.html")

    if request.token is None:
        token = await dependencies.create_temp_jwt_token(
            email=request.email, session=session
        )
    else:
        token = request.token.decode("utf-8")

    async with aiofiles.open(html_path, "r", encoding="utf-8") as file:
        html_content = await file.read()

    html_content = html_content.replace("{{token}}", token)

    email_message: MessageSchema = MessageSchema(
        subject="Подтверждение электронной почты",
        recipients=[request.email],
        body=html_content,
        subtype="html",
    )

    fm = FastMail(config=settings.smtp_conf)
    background_tasks.add_task(dependencies.send_email_task, fm, email_message)

    return {"detail": "email successfully send"}


@router.get("/user-verification", status_code=status.HTTP_200_OK)
async def user_verification(
    token: str,
    session: AsyncSession = Depends(database.get_session),
):
    try:
        payload = jwt.decode(
            jwt=token.encode(),
            key=settings.auth_jwt.publik_key.read_text(),
            algorithms=settings.auth_jwt.algorithm,
        )
    except jwt.ExpiredSignatureError as a:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Token has expired"
        )
    except jwt.InvalidTokenError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid token"
        )

    user_id: int = payload.get("sub")

    stmt = select(UsersOrm).where(UsersOrm.id == user_id)
    res: Result = await session.execute(stmt)

    user: UsersOrm = res.scalars().first()
    user.is_active = True

    await session.commit()

    return {"message": "User is active"}


@router.post("/check-refresh-token", status_code=status.HTTP_200_OK)
async def check_refresh_token(
    token_refresh: str | None = Cookie(alias=COOKIE_JWT_REFRESH, default=None),
):
    if token_refresh is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token is missed",
        )
    try:
        payload = jwt.decode(
            jwt=token_refresh,
            key=settings.auth_jwt.publik_key.read_text(),
            algorithms=settings.auth_jwt.algorithm,
        )
        return payload
    except jwt.ExpiredSignatureError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token refresh expired",
        )
    except jwt.InvalidTokenError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid refresh token"
        )


@router.post("/check-access-token", status_code=status.HTTP_200_OK)
async def check_access_token(
    response: Response,
    token_access: str | None = Cookie(alias=COOKIE_JWT_ACCESS, default=None),
    token_refresh: str | None = Cookie(alias=COOKIE_JWT_REFRESH, default=None),
):
    if token_access is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Access token is missed",
        )
    try:
        payload = jwt.decode(
            jwt=token_access,
            key=settings.auth_jwt.publik_key.read_text(),
            algorithms=settings.auth_jwt.algorithm,
        )
        return payload
    except jwt.ExpiredSignatureError as e:
        payload = await check_refresh_token(token_refresh=token_refresh)
        new_access_token = await dependencies.create_jwt_token(
            user_email=payload.get("email"),
            user_id=payload.get("sub"),
        )
        response.set_cookie(
            key=COOKIE_JWT_ACCESS, value=new_access_token, max_age=604800
        )
    except jwt.InvalidTokenError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid access token"
        )
