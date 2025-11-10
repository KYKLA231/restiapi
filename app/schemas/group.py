from pydantic import BaseModel
from typing import Optional, List


class GroupBase(BaseModel):
    name: str
    description: Optional[str] = None


class GroupCreate(GroupBase):
    pass


class GroupUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None


class GroupInDB(BaseModel):
    id: int
    name: str
    description: Optional[str]
    members: List[int] = []

    class Config:
        orm_mode = True
