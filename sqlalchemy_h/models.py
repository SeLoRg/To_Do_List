from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped
from sqlalchemy import Integer


class Base(DeclarativeBase):
    __abstract__ = True

    id = mapped_column(Integer, primary_key=True)


class WorkersModel(Base):
    __tablename__ = "Workers"
    name: Mapped[str]
    rang: Mapped[str]
    gg: Mapped[str]


class Work(Base):
    __tablenamr__ = "Work"
    name: Mapped[str]
