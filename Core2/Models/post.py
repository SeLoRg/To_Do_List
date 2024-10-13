from .base import Base
from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import String, ForeignKey, Integer
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .user import User


class Post(Base):
    __tablename__: str = "Post"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(100), unique=False)
    body: Mapped[str]
    user_id: Mapped[int] = mapped_column(
        ForeignKey("User.id"),
    )

    # user: Mapped["User"] = relationship(back_populates="posts")
