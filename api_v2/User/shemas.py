from pydantic import BaseModel, ConfigDict


class UserBase(BaseModel):
    user_name: str


class CreateUser(UserBase):
    pass


class UpdateUser(UserBase):
    pass


class User(UserBase):
    id: int
    model_config = ConfigDict(from_attributes=True)
