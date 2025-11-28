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


class CommentBase(BaseModel):
    content: str


class CommentCreate(CommentBase):
    post_id: int


<<<<<<< HEAD
class CommentOut(CommentBase):
    id: int
    post_id: int
    author_id: Optional[int] = None
=======
class CommentInDB(BaseModel):
    id: int
    content: str
    post_id: int
    author_id: Optional[int]
>>>>>>> main
    created_at: datetime

    class Config:
        orm_mode = True
