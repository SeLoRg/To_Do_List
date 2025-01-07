from .base import Base
from sqlalchemy.orm import Mapped


class SessionsOrm(Base):
    __tablename__ = "Sessions"
    user_id: Mapped[int]
