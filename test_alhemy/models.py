import datetime
import enum
from typing import Annotated
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped
from sqlalchemy import Integer, text, String, ForeignKey


created = Annotated[
    datetime.datetime, mapped_column(server_default=text("TIMEZONE('utc', now())"))
]


class Base(DeclarativeBase):
    __abstract__ = True

    id = mapped_column(Integer, primary_key=True)


class WorkersModel(Base):
    __tablename__ = "Workers"
    name: Mapped[str]
    rang: Mapped[str]
    created_at: Mapped[created]

    def __str__(self):
        return f"name={self.name}, rang={self.rang}, id={self.id}, created_at={self.created_at}"


class Workload(enum.Enum):
    # __abstract__ = True
    fulltime: str = "fulltime"
    partime: str = "parttime"


class ResumesModel(Base):
    __tablename__ = "Resumes"
    title = mapped_column(String(256), nullable=False)
    compensation: Mapped[int]
    workload: Mapped[Workload]
    worker_id = mapped_column(Integer, ForeignKey(WorkersModel.id))
    created_at: Mapped[created]
