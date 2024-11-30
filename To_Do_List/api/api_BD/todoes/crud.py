import datetime

from .schemas import TaskSchema, TaskCreateSchema, TasksStatusSchema
from To_Do_List.Models import TasksOrm
from To_Do_List.Models.status import Status
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status
from sqlalchemy import select, and_, Result
import datetime


async def create_task(
    todo_in: TaskCreateSchema, user_id: int, session: AsyncSession
) -> int:
    stmt = select(TasksOrm.id).where(
        and_(TasksOrm.name == todo_in.name, TasksOrm.data == todo_in.data)
    )
    res: Result = await session.execute(stmt)

    if res.scalars().first() is not None:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Tasks already create",
        )

    try:
        task: TasksOrm = TasksOrm(
            **todo_in.model_dump(exclude_none=True), user_id=user_id
        )
        session.add(task)
        await session.commit()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Invalid data"
        )
    return status.HTTP_201_CREATED


async def get_tasks_day(
    user_id: int, day: int, month: int, year: int, session: AsyncSession
) -> list[TasksOrm | None]:
    target_date = datetime.date(year, month, day)
    stmt = select(TasksOrm).where(
        and_(TasksOrm.user_id == user_id, TasksOrm.data == target_date)
    )
    res: Result = await session.execute(stmt)
    task = res.scalars().all()

    return list(task)


async def delete_task(
    task_name: str,
    session: AsyncSession,
) -> None:
    stmt = select(TasksOrm).where(TasksOrm.name == task_name)
    res: Result = await session.execute(stmt)
    task: TasksOrm | None = res.scalars().first()

    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Task is already deleted"
        )

    await session.delete(task)
    await session.commit()


async def task_status_update(task_in: TasksStatusSchema, session: AsyncSession) -> dict:
    stmt = select(TasksOrm).where(
        and_(TasksOrm.name == task_in.name, TasksOrm.data == task_in.date)
    )
    res: Result = await session.execute(stmt)
    task: TasksOrm | None = res.scalars().first()

    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task with this name not founded",
        )

    setattr(task, "status", task_in.status)
    await session.commit()

    return {"detail": "Status update", "status": task_in.status}
