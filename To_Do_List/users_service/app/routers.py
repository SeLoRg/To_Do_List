from fastapi import (
    Depends,
    APIRouter,
    status,
)
from .schemas import UsersCreateSchema, UsersUpdateSchema, UserGetSchema, UsersSchema
from ..Core.Models import UsersOrm
from ..Core.Database.database import database
from sqlalchemy.ext.asyncio import AsyncSession
from . import crud
from .logger import logger


router = APIRouter(tags=["Users"])


@router.put("/create-user", status_code=status.HTTP_201_CREATED)
async def create_user(
    user_in: UsersCreateSchema,
    session: AsyncSession = Depends(database.get_session),
):
    logger.info("/create-user request...")

    res: dict = await crud.create_user(user_in=user_in, session=session)
    return res


@router.get("/get-user", response_model=UsersSchema | None)
async def get_user(
    user_id: int | None = None,
    user_email: str | None = None,
    session: AsyncSession = Depends(database.get_session),
):
    logger.info("/get-user request...")
    user: UsersOrm | None = await crud.get_user(
        user_email=user_email, user_id=user_id, session=session
    )
    return user


@router.patch("/update-user", status_code=status.HTTP_200_OK)
async def update_user(
    user_in: UsersUpdateSchema,
    user_id: int,
    session: AsyncSession = Depends(database.get_session),
):
    logger.info("/update-user request...")
    await crud.update_partial_user(user_in=user_in, session=session, user_id=user_id)
    return {"detail": "User updated"}


@router.delete("/delete-user", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: int,
    session: AsyncSession = Depends(database.get_session),
):
    logger.info("/delete-user request...")

    await crud.delete_user(user_id=user_id, session=session)
