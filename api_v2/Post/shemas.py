from pydantic import BaseModel, ConfigDict


class PostBase(BaseModel):
    title: str
    body: str


class CreatePost(PostBase):
    pass


class UpdatePartialPost(BaseModel):
    title: str | None = None
    body: str | None = None


class Post(PostBase):
    id: int
    user_id: int
    model_config = ConfigDict(from_attributes=True)
