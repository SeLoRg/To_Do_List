from pydantic import BaseModel, ConfigDict


class ProductsPostSchema(BaseModel):
    name: str
    description: str
    price: int
    availability: int


class ProductsGetSchema(ProductsPostSchema):
    id: int
    model_config = ConfigDict(from_attributes=True)


class ProductsUpdatePartialSchema(BaseModel):
    name: str | None = None
    description: str | None = None
    price: int | None = None
    availability: int | None = None
