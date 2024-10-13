from .base import Base
from sqlalchemy import String
from sqlalchemy.orm import mapped_column, Mapped


class User(Base):
    __tablename__: str = "User"
    username: Mapped[str] = mapped_column(String[32], unique=True)
