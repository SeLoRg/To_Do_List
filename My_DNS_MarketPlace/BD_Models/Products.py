from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped
from sqlalchemy import Integer, String
from .Base import Base


class ProductsOrm(Base):
    __tablename__ = "Products"
    name = mapped_column(String(50), nullable=False)
    description = mapped_column(String(256))
    price: Mapped[int]
    availability: Mapped[int] = mapped_column(server_default="1")
