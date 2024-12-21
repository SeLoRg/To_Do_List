from fastapi import APIRouter, Depends, status
from To_Do_List.Core.Database.database import database
from sqlalchemy.ext.asyncio import AsyncSession
from To_Do_List.api.api_BD.todoes import crud
from .schemas import (
    TaskSchema,
    TaskCreateSchema,
    TodoGetSchema,
    TaskDeleteSchema,
    TasksStatusSchema,
)
from To_Do_List.Core.Models import TasksOrm
from To_Do_List.api.api_auth import router as api_auth

router = APIRouter(tags=["Tasks"])


@router.post("/create-task", status_code=status.HTTP_201_CREATED)
async def create_task(
    todo_in: TaskCreateSchema,
    cookie: dict = Depends(api_auth.check_access_token),
    session: AsyncSession = Depends(database.get_session),
):
    task: int = await crud.create_task(
        todo_in=todo_in, user_id=cookie.get("sub"), session=session
    )

    return {"detail": "Task create"}


@router.post(
    "/get-tasks-day", response_model=list[TaskSchema], status_code=status.HTTP_200_OK
)
async def get_tasks_day(
    todo_in: TodoGetSchema,
    cookie: dict = Depends(api_auth.check_access_token),
    session: AsyncSession = Depends(database.get_session),
):
    tasks: list[TasksOrm | None] = await crud.get_tasks_day(
        user_id=cookie.get("sub"),
        day=todo_in.day,
        month=todo_in.month,
        year=todo_in.year,
        session=session,
    )

    return tasks


@router.post("/delete-task", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
    task_in: TaskDeleteSchema,
    session: AsyncSession = Depends(database.get_session),
):
    await crud.delete_task(task_name=task_in.name, session=session)


@router.post("/task-status-update", status_code=status.HTTP_200_OK)
async def task_status(
    task_in: TasksStatusSchema,
    session: AsyncSession = Depends(database.get_session),
):
    body_response: dict = await crud.task_status_update(
        task_in=task_in, session=session
    )
    return body_response
