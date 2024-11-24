from typing import Optional

from pydantic import BaseModel, ConfigDict


class UserBase(BaseModel):
    user_name: str
    role: str
    password: str
    email: str


class CreateUser(UserBase):
    pass


class UpdateUser(UserBase):
    user_name: Optional[str] = None
    role: Optional[str] = None
    password: Optional[str] = None
    email: Optional[str] = None


class User(UserBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
