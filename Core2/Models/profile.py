from .base import Base
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import mapped_column, Mapped, relationship
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .user import User


class Profile(Base):
    __tablename__: str = "Profile"
    first_name: Mapped[str] = mapped_column(String[40])
    last_name: Mapped[str] = mapped_column(String[40])
    bio: Mapped[str]
    user_id: Mapped[int] = mapped_column(ForeignKey("User.id"), unique=True)

    user: Mapped["User"] = relationship(back_populates="profile")
