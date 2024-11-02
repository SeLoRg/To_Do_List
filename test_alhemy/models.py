import datetime
import enum
from typing import Annotated
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped, relationship
from sqlalchemy import Integer, text, String, ForeignKey, Column, UniqueConstraint


created = Annotated[
    datetime.datetime, mapped_column(server_default=text("TIMEZONE('utc', now())"))
]


class Base(DeclarativeBase):
    __abstract__ = True

    id = mapped_column(Integer, primary_key=True)


class WorkersModel(Base):
    __tablename__ = "Workers"
    name: Mapped[str]
    rang: Mapped[str]
    created_at: Mapped[created]

    resumes: Mapped[list["ResumesModel"]] = relationship(
        "ResumesModel", back_populates="worker"
    )

    def __str__(self):
        return f"name={self.name}, rang={self.rang}, id={self.id}, created_at={self.created_at}"


class Workload(enum.Enum):
    # __abstract__ = True
    fulltime: str = "fulltime"
    partime: str = "parttime"


class ResumesModel(Base):
    __tablename__ = "Resumes"
    title = mapped_column(String(256), nullable=False)
    compensation: Mapped[int]
    workload: Mapped[Workload]
    worker_id = mapped_column(Integer, ForeignKey(WorkersModel.id))
    created_at: Mapped[created]

    worker: Mapped["WorkersModel"] = relationship(
        "WorkersModel", back_populates="resumes"
    )

    def __str__(self):
        return f"title={self.title}, compensation={self.compensation}, id={self.id}, created_at={self.created_at}, workload={self.workload}, worker_id={self.worker_id}"


class ProductsModel(Base):
    __tablename__ = "Products"

    name: Mapped[str]
    description: Mapped[str]
    price: Mapped[int]

    orders: Mapped[list["OrdersModel"]] = relationship(
        back_populates="products",
        secondary="OrderProduct",
    )

    def __str__(self):
        return f"name={self.name}, description={self.description}, price={self.price}"


class OrdersModel(Base):
    __tablename__ = "Orders"

    promo: Mapped[str | None] = None
    created_at: Mapped[created]

    products: Mapped[list["ProductsModel"]] = relationship(
        back_populates="orders",
        secondary="OrderProduct",
    )


class OrderProduct(Base):
    __tablename__ = "OrderProduct"

    product_id: Mapped[int] = mapped_column(
        ForeignKey(ProductsModel.id), nullable=False
    )
    order_id: Mapped[int] = mapped_column(
        ForeignKey(OrdersModel.id),
        nullable=False,
    )
    count: Mapped[int] = mapped_column(default=1)

    UniqueConstraint("product_id", "order_id", name="index_unique_order_product")
