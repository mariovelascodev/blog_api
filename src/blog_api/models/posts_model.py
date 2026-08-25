from pydantic import BaseModel
from datetime import datetime


class Post(BaseModel):
    id: int
    title: str
    content: str
    category: str
    tags: list[str]
    createdAt: datetime
    updateAt: datetime


class CreatePost(BaseModel):
    title: str
    content: str
    category: str
    tags: list[str]


class UpdatePost(BaseModel):
    id: int
    title: str
    content: str
    category: str
    tags: list[str]
