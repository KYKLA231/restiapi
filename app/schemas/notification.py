from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class NotificationBase(BaseModel):
    message: str


class NotificationCreate(NotificationBase):
    user_id: int


class NotificationInDB(BaseModel):
    id: int
    user_id: int
    message: str
    read: bool
    created_at: datetime

    class Config:
        orm_mode = True
