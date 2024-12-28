from .base import Base
from sqlalchemy.orm import Mapped
import datetime


class RefreshBlackListOrm(Base):
    __tablename__ = "RefreshBlackList"

    user_id: Mapped[int]
    refresh_id: Mapped[int]
    expire: Mapped[float]
