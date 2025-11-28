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


class EventBase(BaseModel):
    title: str
    description: Optional[str] = None
    starts_at: Optional[datetime] = None


class EventCreate(EventBase):
    pass


<<<<<<< HEAD
class EventOut(EventBase):
    id: int
    created_by: Optional[int] = None
=======
class EventInDB(BaseModel):
    id: int
    title: str
    description: Optional[str]
    starts_at: Optional[datetime]
    created_by: Optional[int]
>>>>>>> main
    created_at: datetime

    class Config:
        orm_mode = True
