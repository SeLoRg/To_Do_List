from pydantic import ConfigDict, BaseModel


class UserGetSchema(BaseModel):
    email: str | None = None
    id: int | None = None
    model_config = ConfigDict(extra="ignore")


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
    username: str
    email: str

    model_config = ConfigDict(from_attributes=True)
