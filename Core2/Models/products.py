from Core2.Models.base import Base
from sqlalchemy.orm import mapped_column
from sqlalchemy import String, Float


class Products(Base):
    __tablename__ = "Products"

    name = mapped_column(String(50))
    price = mapped_column(Float)
