from .base import Base
from sqlalchemy import ForeignKey
from sqlalchemy.orm import mapped_column, Mapped, relationship
from .todoes import TasksOrm


from .friends_list import FriendsListOrm


class UsersOrm(Base):
    __tablename__: str = "Users"

    username: Mapped[str]
    email: Mapped[str]
    password: Mapped[bytes]
    is_active: Mapped[bool]
    # logo_url: Mapped[str]

    tasks: Mapped[list["TasksOrm"]] = relationship(
        "TasksOrm",
        back_populates="user",
    )

    friends: Mapped[list["UsersOrm"]] = relationship(
        "UsersOrm",
        secondary="FriendsList",
        primaryjoin="UsersOrm.id == FriendsListOrm.user_id",
        secondaryjoin="UsersOrm.id == FriendsListOrm.friend_id",
        backref="followers",
    )
