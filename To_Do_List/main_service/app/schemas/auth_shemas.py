from pydantic import BaseModel, ConfigDict


class UserLoginSchema(BaseModel):
    email: str
    password: str


class UserLoginResponse(BaseModel):
    access_token: str


class UserRegistrateSchema(BaseModel):
    username: str
    email: str
    password: str


class ResponseCredentials(BaseModel):
    user_email: str
    session_id: int
    user_id: int
    model_config = ConfigDict(from_attributes=True)


class LogoutRequest(BaseModel):
    user_email: str
    session_id: int
    user_id: int
    model_config = ConfigDict(from_attributes=True)


class RequestCredentials(BaseModel):
    user_email: str
    session_id: int
    user_id: int
    model_config = ConfigDict(from_attributes=True)


class CheckAuthResponse(BaseModel):
    auth_status: bool = True
    new_token: str | None = None
    token_exp: bool = False
    credentials: RequestCredentials = None
    model_config = ConfigDict(from_attributes=True)


class UsersSchema(BaseModel):
    id: int
    username: str
    email: str
    password: bytes

    model_config = ConfigDict(from_attributes=True)
