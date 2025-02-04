import datetime

from .base import Base
from sqlalchemy.orm import Mapped, mapped_column


class SessionsOrm(Base):
    __tablename__ = "Sessions"
    refresh_token: Mapped[str]
    user_id: Mapped[int]
    ip: Mapped[str]
    agent: Mapped[str]
    expire: Mapped[float]
    is_valid: Mapped[bool]
