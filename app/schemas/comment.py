from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class CommentBase(BaseModel):
    content: str


class CommentCreate(CommentBase):
    post_id: int


class CommentInDB(BaseModel):
    id: int
    content: str
    post_id: int
    author_id: Optional[int]
    created_at: datetime

    class Config:
        orm_mode = True
