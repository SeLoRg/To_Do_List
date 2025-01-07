from .base import Base
from sqlalchemy.orm import Mapped


class UsersOrm(Base):
    __tablename__: str = "Users"

    username: Mapped[str]
    email: Mapped[str]
    password: Mapped[bytes]
    is_active: Mapped[bool]

    def __repr__(self):
        return f"Users: username={self.username}, email={self.email}, is_active={self.is_active}"
