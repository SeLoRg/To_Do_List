from pydantic import ConfigDict, BaseModel


class UserLoginSchema(BaseModel):
    email: str
    password: str


class UsersCreateSchema(BaseModel):
    password: str
    username: str
    email: str


class UsersUpdateSchema(BaseModel):
    password: str | None = None
    username: str | None = None
    email: str | None = None


class UsersDeleteSchema(UsersCreateSchema):
    pass


class UsersSchema(BaseModel):
    id: int
    password: str
    username: str
    email: str

    model_config = ConfigDict(from_attributes=True)
