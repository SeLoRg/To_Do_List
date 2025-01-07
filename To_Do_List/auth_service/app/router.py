from fastapi import (
    Response,
    Cookie,
    APIRouter,
    BackgroundTasks,
    status,
    Depends,
    HTTPException,
)
from .shemas import UserLoginSchema
from . import service
from sqlalchemy.ext.asyncio import AsyncSession
from ..Core.Database.database import database_sessions, database_users
from .logger import logger

router = APIRouter(tags=["Auth"], prefix="/auth")


@router.post("/login", status_code=status.HTTP_200_OK)
async def login(
    data: UserLoginSchema,
    response: Response,
    session_users: AsyncSession = Depends(database_users.get_session),
    session_sessions: AsyncSession = Depends(database_sessions.get_session),
):
    try:
        logger.info("/login request...")
        await service.login(
            data=data,
            response=response,
            session_users=session_users,
            session_sessions=session_sessions,
        )
        return {"detail": "authentication success"}
    except HTTPException as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )
