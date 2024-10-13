from Core2.Models import UserModel
from .shemas import CreateUser, User
from sqlalchemy.ext.asyncio import AsyncSession


async def create_user(user_in: CreateUser, session: AsyncSession) -> UserModel:
    user = UserModel(**user_in.model_dump())
    session.add(user)
    await session.commit()
    return user


async def get_user(user_id: int, session: AsyncSession) -> UserModel | None:
    return await session.get(UserModel, user_id)
