from pydantic import BaseModel


class PostBase(BaseModel):
    title: str
    body: str


class CreatePost(PostBase):
    pass


class Post(PostBase):
    id: int
    user_id: int
