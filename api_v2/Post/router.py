from fastapi import APIRouter, status, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from .shemas import Post, CreatePost, UpdatePartialPost
from . import crud
from Core2.db_helper import db_helper

router = APIRouter(tags=["Post"])


@router.post("/", response_model=Post)
async def create_post(
    post_in: CreatePost,
    user_id: int,
    session: AsyncSession = Depends(db_helper.get_session),
):
    return await crud.create_post(post_in=post_in, user_id=user_id, session=session)


@router.get("/{post_id}/", response_model=Post | None)
async def get_post(
    post_id: int, session: AsyncSession = Depends(db_helper.get_session)
):
    return await crud.get_post(post_id=post_id, session=session)


@router.get("/", response_model=list[Post])
async def get_posts(session: AsyncSession = Depends(db_helper.get_session)):
    return await crud.get_posts(session=session)


@router.patch("/{post_id}/", response_model=Post)
async def update_partial_post(
    post_in: UpdatePartialPost,
    post_id: int,
    session: AsyncSession = Depends(db_helper.get_session),
):
    return await crud.update_partial_post(
        post_id=post_id, post_in=post_in, session=session
    )


@router.delete("/{post_id}/", status_code=status.HTTP_204_NO_CONTENT)
async def del_post(
    post_id: int, session: AsyncSession = Depends(db_helper.get_session)
):
    return await crud.del_post(post_id=post_id, session=session)
