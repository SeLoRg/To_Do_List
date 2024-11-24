from sqlalchemy import ForeignKey, func, DateTime
from .base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .status import Status
import datetime


class TodoesOrm(Base):
    __tablename__: str = "Todoes"

    name: Mapped[str]
    status_id: Mapped[Status] = mapped_column(
        nullable=False, server_default=Status.unfinished.name
    )
    description: Mapped[str]
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    expiration_at: Mapped[datetime.datetime] = mapped_column(nullable=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("Users.id"), nullable=False)

    # user: Mapped["UsersOrm"] = relationship("UsersOrm", back_populates="todoes")
