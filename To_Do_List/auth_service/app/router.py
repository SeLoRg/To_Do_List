from fastapi import (
    Response,
    Cookie,
    APIRouter,
    BackgroundTasks,
    status,
    Depends,
    HTTPException,
    Request,
)
from sqlalchemy.ext.asyncio import AsyncSession
from .shemas import (
    UserLoginSchema,
    ResponseCredentials,
    RequestCredentials,
    CheckAuthResponse,
)
from . import service
from ..Core.Database.database import database_sessions, database_users
from ..Core.config import settings

router = APIRouter(tags=["Auth"], prefix="/auth")


@router.post("/login", status_code=status.HTTP_200_OK)
async def login(
    response: Response,
    data: UserLoginSchema,
    session_user: AsyncSession = Depends(database_users.get_session),
    session_sessions: AsyncSession = Depends(database_sessions.get_session),
):
    try:
        res: dict = await service.login(
            data=data, session_sessions=session_sessions, session_user=session_user
        )
        access_token: str = res.get("access_token")
        response.set_cookie(key=settings.COOKIE_JWT_ACCESS, value=access_token)
        return access_token
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=f"{e.detail}")
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"{str(e)}"
        )


@router.post("/logout", status_code=status.HTTP_200_OK)
async def logout(
    response: Response,
    request: Request,
    session_sessions: AsyncSession = Depends(database_sessions.get_session),
):
    try:
        access_token: str | None = request.cookies.get(settings.COOKIE_JWT_ACCESS)
        res: CheckAuthResponse | None = await service.check_authenticate(
            access_token=access_token, session_sessions=session_sessions
        )
        res: dict = await service.logout(
            credentials=res.credentials,
            session_sessions=session_sessions,
        )
        response.delete_cookie(key=settings.COOKIE_JWT_ACCESS)
        return res
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=f"{e.detail}")
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"{str(e)}"
        )


@router.get(
    "/check-authenticate",
    status_code=status.HTTP_200_OK,
    response_model=CheckAuthResponse,
)
async def check_authenticate(
    request: Request,
    session_sessions: AsyncSession = Depends(database_sessions.get_session),
):
    try:
        res: CheckAuthResponse | None = await service.check_authenticate(
            access_token=request.cookies.get(f"{settings.COOKIE_JWT_ACCESS}"),
            session_sessions=session_sessions,
        )
        if res is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
            )
        return res
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=f"{e.detail}")
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"{str(e)}"
        )


@router.get("/decode-jwt", status_code=status.HTTP_200_OK)
async def decode_jwt(token: str):
    try:
        credentials: dict | None = await service.get_credentials_from_jwt(token)
        return credentials
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=f"{e.detail}")
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"{str(e)}"
        )
