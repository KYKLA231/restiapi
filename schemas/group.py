<<<<<<< HEAD
from __future__ import annotations

from typing import List, Optional

from pydantic import BaseModel
=======
from pydantic import BaseModel
from typing import Optional, List
>>>>>>> main


class GroupBase(BaseModel):
    name: str
    description: Optional[str] = None


class GroupCreate(GroupBase):
    pass


class GroupUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None


<<<<<<< HEAD
class GroupOut(GroupBase):
    id: int
    member_ids: List[int] = []
=======
class GroupInDB(BaseModel):
    id: int
    name: str
    description: Optional[str]
    members: List[int] = []
>>>>>>> main

    class Config:
        orm_mode = True
