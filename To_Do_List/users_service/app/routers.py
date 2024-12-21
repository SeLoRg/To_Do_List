import json

from aiokafka.errors import KafkaError
from fastapi import (
    Depends,
    APIRouter,
    status,
    Response,
    HTTPException,
    Cookie,
)

from .schemas import UsersCreateSchema, UsersUpdateSchema
from ...Core.Models import UsersOrm
from ...Core.config.config import settings
from ...Core.Database.database import database
from ...Core.jwt_check.jwt import check_access_token
from sqlalchemy.ext.asyncio import AsyncSession
from . import crud
from aiokafka import AIOKafkaProducer


router = APIRouter(tags=["Users"])

producer = AIOKafkaProducer(
    bootstrap_servers=settings.KAFKA_BROKER,
    acks="all",
    enable_idempotence=True,
)


@router.post("/create-user", status_code=status.HTTP_201_CREATED)
async def create_user(
    user_in: UsersCreateSchema,
    session: AsyncSession = Depends(database.get_session),
):
    user_create: UsersOrm = await crud.create_user(user_in=user_in, session=session)
    try:
        await producer.send_and_wait(
            "notification_topic",
            value=json.dumps(
                {"email": user_create.email, "user_id": user_create.id}
            ).encode("utf-8"),
        )
    except KafkaError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Somthing wrong! Please try again.",
        )
    return {"detail": "User create"}


# тут в будущем нужно добавить сущность в бд под именем Profile.
# Именно профиль будет хранить подробную информацию о пользователе
@router.post("/update-user", status_code=status.HTTP_200_OK)
async def update_user(
    email: str,
    user_in: UsersUpdateSchema,
    jwt_access: str | None = Cookie(alias=settings.COOKIE_JWT_ACCESS, default=None),
    jwt_refresh: str | None = Cookie(alias=settings.COOKIE_JWT_REFRESH, default=None),
    session: AsyncSession = Depends(database.get_session),
):

    jwt_access_payload: dict | None = await check_access_token(
        jwt_access=jwt_access, jwt_refresh=jwt_refresh
    )

    # if jwt_access_payload is None:
    # jwt_refresh_payload:

    user_update: UsersOrm = await crud.update_partial_user(
        email=email, user_in=user_in, session=session
    )

    return {"detail": "User update"}


@router.delete("/delete-user", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    response: Response,
    cookie: dict = Depends(),
    session: AsyncSession = Depends(database.get_session),
):
    await crud.delete_user(id_user=cookie.get("sub"), session=session)
    # response.delete_cookie()

    return {"detail": "User deleted"}
