from sqlalchemy import ForeignKey, func, Date
from .base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .status import Status
import datetime
from typing import TYPE_CHECKING

if TYPE_CHECKING:

    from .users import UsersOrm


class TasksOrm(Base):
    __tablename__: str = "Tasks"

    name: Mapped[str]
    status: Mapped[Status] = mapped_column(
        nullable=False, server_default=Status.unfinished.name
    )
    data: Mapped[datetime.date] = mapped_column(Date(), server_default=func.now())
    user_id: Mapped[int] = mapped_column(ForeignKey("Users.id"), nullable=False)

    user: Mapped["UsersOrm"] = relationship("UsersOrm", back_populates="tasks")
