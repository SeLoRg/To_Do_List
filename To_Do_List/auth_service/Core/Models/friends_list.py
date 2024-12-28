from sqlalchemy.orm import Mapped, relationship, mapped_column
from sqlalchemy import ForeignKey
from .base import Base
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .users import UsersOrm


class FriendsListOrm(Base):
    __tablename__ = "FriendsList"
    friend_id: Mapped[int] = mapped_column(
        ForeignKey("Users.id"), primary_key=True, nullable=False
    )
    user_id: Mapped[int] = mapped_column(
        ForeignKey("Users.id"), primary_key=True, nullable=False
    )
    is_confirmed: Mapped[bool] = mapped_column(server_default="False")
