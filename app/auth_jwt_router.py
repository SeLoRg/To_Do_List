import datetime

import jwt
from fastapi import APIRouter, Depends, Form, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from Core2.config import settings
from pydantic import BaseModel, ConfigDict, EmailStr
import bcrypt

router = APIRouter(tags=["JWT"])
http_bearer = HTTPBearer()


class TokenInfo(BaseModel):
    token: bytes
    type: str


class UserSchema(BaseModel):
    username: str
    password: bytes
    email: EmailStr | None
    active: bool = True
    model_config = ConfigDict(strict=True)


def hash_pass(password: str) -> bytes:
    salt = bcrypt.gensalt()
    b_password: bytes = password.encode()
    return bcrypt.hashpw(b_password, salt)


def check_hash_pass(password: str, hash_: bytes) -> bool:
    return bcrypt.checkpw(password=password.encode(), hashed_password=hash_)


john = UserSchema(
    username="John", password=hash_pass(password="2528"), email="john@mail.com"
)
sam = UserSchema(
    username="John", password=hash_pass(password="secret"), email="sam@bk.ru"
)

USERS_DB: dict[str, UserSchema] = {
    "john": john,
    "sam": sam,
}


def validate_auth_user(
    username: str,
    password: str,
):
    exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username or password"
    )

    if not (user := USERS_DB.get(username)):
        raise exception

    if check_hash_pass(password=password, hash_=user.password):
        return user

    raise exception


@router.post("/login/", response_model=TokenInfo)
async def auth_user_jwt(
    user: UserSchema = Depends(validate_auth_user),
):
    payload: dict = {
        "sub": user.username,
        "email": user.email,
        "iat": datetime.datetime.now(tz=datetime.timezone.utc).timestamp(),
        "expt": (
            datetime.datetime.now(tz=datetime.timezone.utc)
            + datetime.timedelta(minutes=15)
        ).timestamp(),
    }

    token = jwt.encode(
        payload=payload,
        key=settings.auth_jwt.private_key.read_text(),
        algorithm=settings.auth_jwt.algorithm,
    )

    return TokenInfo(token=token, type="Bearer")


@router.get("/users/me")
def get_current_auth_user(
    credentials: HTTPAuthorizationCredentials = Depends(http_bearer),
):

    return jwt.decode(
        jwt=credentials.credentials,
        key=settings.auth_jwt.public_key.read_text(),
        algorithms=settings.auth_jwt.algorithm,
    )
