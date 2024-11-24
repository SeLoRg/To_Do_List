from pydantic import BaseModel, EmailStr


class UserVerificationEmailSchema(BaseModel):
    email: EmailStr
    sub: str
    message: str
