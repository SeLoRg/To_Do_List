from .base import Base
from sqlalchemy import ForeignKey
from sqlalchemy.orm import mapped_column, Mapped, relationship
from .todoes import TodoesOrm
from .profiles import ProfilesOrm


class UsersOrm(Base):
    __tablename__: str = "Users"

    username: Mapped[str]
    email: Mapped[str]
    password: Mapped[bytes]
    is_active: Mapped[bool]
    # profile_id: Mapped[int] = mapped_column(ForeignKey("Profiles.id"), nullable=False)
    #
    # todoes: Mapped[list["TodoesOrm"]] = relationship(
    #     "TodoesOrm",
    #     back_populates="user",
    # )
    # profile: Mapped["ProfilesOrm"] = relationship("ProfilesOrm", back_populates="user")
