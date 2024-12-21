from .base import Base
from sqlalchemy.orm import Mapped, relationship
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .users import UsersOrm


class ProfilesOrm(Base):
    __tablename__: str = "Profiles"

    username: Mapped[str]
    email: Mapped[str]

    # user: Mapped["UsersOrm"] = relationship("UsersOrm", back_populates="profile")
