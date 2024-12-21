import datetime

from pydantic import BaseModel, ConfigDict

from To_Do_List.Core.Models.status import Status


class TodoGetSchema(BaseModel):
    day: int
    month: int
    year: int


class TasksStatusSchema(BaseModel):
    name: str
    date: datetime.date
    status: Status


class TaskDeleteSchema(BaseModel):
    name: str


class TaskCreateSchema(BaseModel):
    name: str
    status: Status = Status.unfinished
    data: datetime.date


class TaskSchema(BaseModel):
    id: int
    name: str
    status: Status

    model_config = ConfigDict(from_attributes=True)
