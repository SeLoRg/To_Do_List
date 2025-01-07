from pydantic import BaseModel, ConfigDict


class UserLoginSchema(BaseModel):
    email: str
    password: str


class UsersSchema(BaseModel):
    id: int
    username: str
    email: str
    password: bytes

    model_config = ConfigDict(from_attributes=True)
