from pydantic import BaseModel, ConfigDict


class Tokens(BaseModel):
    access_token: str
    refresh_token: str


class UserLoginSchema(BaseModel):
    email: str
    password: str
    ip: str
    agent: str


class UserLoginResponse(Tokens):
    is_login: bool
    pass


class UserRegistrateSchema(BaseModel):
    username: str
    email: str
    password: str


class Credentials(BaseModel):
    user_id: int
    model_config = ConfigDict(from_attributes=True)


class LogoutRequest(Credentials):
    pass


class CheckAuthRequest(BaseModel):
    ip: str
    agent: str
    access_token: str | None = None
    refresh_token: str | None = None


class CheckAuthResponse(BaseModel):
    is_login: bool = False
    new_tokens: Tokens | None = None
    credentials: Credentials | None = None
    model_config = ConfigDict(from_attributes=True)


class UsersSchema(BaseModel):
    id: int
    username: str
    email: str
    password: bytes

    model_config = ConfigDict(from_attributes=True)
