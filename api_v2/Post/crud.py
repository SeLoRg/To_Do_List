from sqlalchemy.ext.asyncio import AsyncSession
from Core2.Models import PostModel
from .shemas import CreatePost, Post, UpdatePartialPost
from sqlalchemy import select, Result
from fastapi import HTTPException, status


async def create_post(
    post_in: CreatePost, user_id: int, session: AsyncSession
) -> PostModel:
    post = PostModel(**post_in.model_dump(), user_id=user_id)
    session.add(post)
    await session.commit()
    return post


async def get_post(post_id: int, session: AsyncSession) -> PostModel | None:
    post: PostModel | None = await session.get(PostModel, post_id)
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return post


async def get_posts(session: AsyncSession) -> list[PostModel]:
    stmt = select(PostModel).order_by(PostModel.id)
    result: Result = await session.execute(stmt)
    posts = result.scalars().all()
    return list(posts)


async def update_partial_post(
    post_id: int,
    post_in: UpdatePartialPost,
    session: AsyncSession,
):
    post = await get_post(post_id=post_id, session=session)

    for name, value in post_in.model_dump(exclude_none=True).items():
        setattr(post, name, value)

    await session.commit()
    return post


async def del_post(post_id: int, session: AsyncSession) -> None:
    post: PostModel | None = await get_post(post_id=post_id, session=session)
    await session.delete(post)
    await session.commit()
