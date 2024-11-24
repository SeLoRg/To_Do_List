from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from . import crud
from .shemas import User, CreateUser, UpdateUser
from Core2.db_helper import db_helper

router = APIRouter(tags=["User"])


@router.post("/", response_model=User)
async def create_user(
    user_in: CreateUser,
    session: AsyncSession = Depends(db_helper.get_session),
):
    return await crud.create_user(user_in=user_in, session=session)


@router.get("/{user_id}/", response_model=User | None)
async def get_user(
    user_id: int, session: AsyncSession = Depends(db_helper.get_session)
):
    return await crud.get_user(user_id=user_id, session=session)


@router.get("/", response_model=list[User])
async def get_users(session: AsyncSession = Depends(db_helper.get_session)):
    return await crud.get_users(session=session)


@router.patch("/{user_id}/", response_model=User | None)
async def update_user(
    user_id: int,
    user_in: UpdateUser,
    session: AsyncSession = Depends(db_helper.get_session),
):
    return await crud.update_user(user_id=user_id, session=session, user_in=user_in)


@router.delete("/{user_id}/", status_code=status.HTTP_204_NO_CONTENT)
async def del_user(
    user_id: int, session: AsyncSession = Depends(db_helper.get_session)
):
    return await crud.del_user(user_id=user_id, session=session)
