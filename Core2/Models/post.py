from .base import Base
from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy import String, ForeignKey


class Post(Base):
    __tablename__: str = "Post"
    title: Mapped[str] = mapped_column(String(100), unique=False)
    body: Mapped[str]
    user_id: Mapped[int] = mapped_column(
        ForeignKey("User.id"),
    )
