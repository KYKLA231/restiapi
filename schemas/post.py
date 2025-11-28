<<<<<<< HEAD
from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import BaseModel
=======
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
>>>>>>> main


class PostBase(BaseModel):
    title: str
    content: Optional[str] = None


class PostCreate(PostBase):
    pass


class PostUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None


<<<<<<< HEAD
class PostOut(PostBase):
    id: int
    owner_id: Optional[int] = None
=======
class PostInDB(BaseModel):
    id: int
    title: str
    content: Optional[str]
    owner_id: Optional[int]
>>>>>>> main
    created_at: datetime

    class Config:
        orm_mode = True
