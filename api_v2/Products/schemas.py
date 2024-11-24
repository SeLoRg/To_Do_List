from pydantic import BaseModel, ConfigDict
from typing import Optional


class ProductsBase(BaseModel):
    name: str
    price: float


class ProductsCreate(ProductsBase):
    pass


class ProductsUpdate(ProductsBase):
    pass


class ProductsUpdatePartial(BaseModel):
    name: str | None = None
    price: float | None = None


class Products(ProductsBase):
    id: int
    model_config = ConfigDict(from_attributes=True)
