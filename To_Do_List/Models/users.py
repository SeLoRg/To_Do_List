from .base import Base
from sqlalchemy import ForeignKey
from sqlalchemy.orm import mapped_column, Mapped, relationship
from .todoes import TasksOrm


class UsersOrm(Base):
    __tablename__: str = "Users"

    username: Mapped[str]
    email: Mapped[str]
    password: Mapped[bytes]
    is_active: Mapped[bool]

    tasks: Mapped[list["TasksOrm"]] = relationship(
        "TasksOrm",
        back_populates="user",
    )
