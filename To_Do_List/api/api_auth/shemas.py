from pydantic import BaseModel, EmailStr


class EmailVerificationRequest(BaseModel):
    token: bytes | None = None
    email: str


class UserLogin(BaseModel):
    email: str
    password: str
