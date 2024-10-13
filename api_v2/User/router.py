from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from . import crud
from .shemas import User, CreateUser
from Core2.db_helper import db_helper

router = APIRouter(tags=["User"])


@router.post("/", response_model=User)
async def create_user(
    user_in: CreateUser,
    session: AsyncSession = Depends(db_helper.get_session),
):
    return await crud.create_user(user_in=user_in, session=session)


@router.get("/{user_id}/", response_model=User)
async def get_user(
    user_id: int, session: AsyncSession = Depends(db_helper.get_session)
):
    return await crud.get_user(user_id=user_id, session=session)
