from fastapi import Depends, APIRouter, status, BackgroundTasks, Response
from fastapi.responses import FileResponse
from .schemas import UsersCreateSchema, UsersSchema, UsersUpdateSchema
from To_Do_List.Models import UsersOrm
from sqlalchemy.ext.asyncio import AsyncSession
from To_Do_List.Core.database import database
from To_Do_List.api.api_BD.users import crud
from To_Do_List.api.api_auth import dependencies
from To_Do_List.api.api_auth.router import send_email_verification
from To_Do_List.api.api_auth.router import EmailVerificationRequest
from To_Do_List.api.api_auth.router import COOKIE_JWT_REFRESH, COOKIE_JWT_ACCESS

router = APIRouter(tags=["Users"])


@router.post("/create-user", status_code=status.HTTP_201_CREATED)
async def create_user(
    user_in: UsersCreateSchema,
    background_tasks: BackgroundTasks,
    session: AsyncSession = Depends(database.get_session),
):

    user_create: UsersOrm = await crud.create_user(user_in=user_in, session=session)

    token = await dependencies.create_jwt_token(
        user_email=user_create.email, user_id=user_create.id
    )
    res = await send_email_verification(
        request=EmailVerificationRequest(token=token, email=user_create.email),
        background_tasks=background_tasks,
    )
    return {"detail": "User create"}


@router.post("/update-user", status_code=status.HTTP_200_OK)
async def update_user(
    email: str,
    user_in: UsersUpdateSchema,
    response: Response,
    session: AsyncSession = Depends(database.get_session),
):
    user_update: UsersOrm = await crud.update_partial_user(
        email=email, user_in=user_in, session=session
    )

    response.delete_cookie(key=COOKIE_JWT_REFRESH)
    response.delete_cookie(key=COOKIE_JWT_ACCESS)

    return {"detail": "User update"}
