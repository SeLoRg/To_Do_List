from .base import Base
from sqlalchemy import String, ForeignKey, Integer
from sqlalchemy.orm import mapped_column, Mapped, relationship
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .user import User


class Profile(Base):
    __tablename__: str = "Profile"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    first_name: Mapped[str] = mapped_column(String[40])
    last_name: Mapped[str] = mapped_column(String[40])
    bio: Mapped[str | None]
    user_id: Mapped[int] = mapped_column(ForeignKey("User.id"), unique=True)

    user: Mapped["User"] = relationship(back_populates="profile")
