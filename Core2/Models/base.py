from sqlalchemy.orm import mapped_column, DeclarativeBase, declared_attr
from sqlalchemy import Integer


class Base(DeclarativeBase):
    __abstract__ = True
    id = mapped_column(Integer, primary_key=True)
