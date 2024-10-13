from pydantic import BaseModel


class ProfileBase(BaseModel):
    first_name: str
    last_name: str
    bio: str | None = None


class CreateProfile(ProfileBase):
    pass


class Profile(ProfileBase):
    id: int
    user_id: int
