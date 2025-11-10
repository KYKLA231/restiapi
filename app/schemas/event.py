from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class EventBase(BaseModel):
    title: str
    description: Optional[str] = None
    starts_at: Optional[datetime] = None


class EventCreate(EventBase):
    pass


class EventInDB(BaseModel):
    id: int
    title: str
    description: Optional[str]
    starts_at: Optional[datetime]
    created_by: Optional[int]
    created_at: datetime

    class Config:
        orm_mode = True
