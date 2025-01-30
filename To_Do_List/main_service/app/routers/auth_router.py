from fastapi import APIRouter, Request, Response, status
from fastapi.exceptions import HTTPException
from ..schemas.auth_shemas import UserLoginSchema, CheckAuthResponse

auth_router = APIRouter(tags=["auth"])


@auth_router.post("/login", status_code=status.HTTP_200_OK)
async def login(
    response: Response,
    data: UserLoginSchema,
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


@auth_router.post("/logout", status_code=status.HTTP_200_OK)
async def logout(
    response: Response,
    request: Request,
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


@auth_router.post("/registrate")
async def registrate():
    pass
