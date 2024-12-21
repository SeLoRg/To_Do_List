from .base import Base
from sqlalchemy.orm import Mapped
import datetime


class RefreshListOrm(Base):
    __tablename__ = "RefreshList"

    user_id: Mapped[int]
    expire: Mapped[float]
