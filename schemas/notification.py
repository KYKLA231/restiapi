<<<<<<< HEAD
from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel
=======
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
>>>>>>> main


class NotificationBase(BaseModel):
    message: str


class NotificationCreate(NotificationBase):
    user_id: int


<<<<<<< HEAD
class NotificationOut(NotificationBase):
    id: int
    user_id: int
=======
class NotificationInDB(BaseModel):
    id: int
    user_id: int
    message: str
>>>>>>> main
    read: bool
    created_at: datetime

    class Config:
        orm_mode = True
