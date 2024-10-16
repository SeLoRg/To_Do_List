from Core2.Models import UserModel, PostModel, ProfileModel
from .shemas import CreateUser, User, UpdateUser
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, Result
from fastapi import HTTPException, status


async def create_user(user_in: CreateUser, session: AsyncSession) -> UserModel:
    user = UserModel(**user_in.model_dump())
    session.add(user)
    await session.commit()
    return user


async def get_user(user_id: int, session: AsyncSession) -> UserModel | None:
    user: UserModel | None = await session.get(UserModel, user_id)

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return user


async def get_users(session: AsyncSession) -> list[UserModel]:
    stmt = select(UserModel).order_by(UserModel.id)
    result: Result = await session.execute(stmt)
    users = result.scalars().all()
    return list(users)


async def update_user(
    user_id: int, user_in: UpdateUser, session: AsyncSession
) -> UserModel | None:
    user = await session.get(UserModel, user_id)
    for name, value in user_in.model_dump(exclude_none=True):
        setattr(user, name, value)
    await session.commit()
    return user


async def del_user(user_id: int, session: AsyncSession) -> None:
    user = await get_user(user_id=user_id, session=session)

    stmt_post = (
        select(PostModel.id).where(PostModel.user_id == user_id).order_by(PostModel.id)
    )
    stmt_profile = (
        select(ProfileModel.id)
        .where(ProfileModel.user_id == user_id)
        .order_by(ProfileModel.id)
    )

    result_profile: Result = await session.execute(stmt_profile)
    result_post: Result = await session.execute(stmt_post)

    profile_id = result_profile.scalars().all()
    post_id = result_post.scalars().all()

    if not not post_id:
        for PostId in post_id:
            post = await session.get(PostModel, PostId)
            await session.delete(post)
            await session.commit()

    if not not profile_id:
        for ProfileId in profile_id:
            profile = await session.get(ProfileModel, ProfileId)
            await session.delete(profile)
            await session.commit()

    await session.delete(user)
    await session.commit()
