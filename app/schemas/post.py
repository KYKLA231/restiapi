from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class PostBase(BaseModel):
    title: str
    content: Optional[str] = None


class PostCreate(PostBase):
    pass


class PostUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None


class PostInDB(BaseModel):
    id: int
    title: str
    content: Optional[str]
    owner_id: Optional[int]
    created_at: datetime

    class Config:
        orm_mode = True
