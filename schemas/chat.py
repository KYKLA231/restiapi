<<<<<<< HEAD
from __future__ import annotations

from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel


class ChatBase(BaseModel):
    title: Optional[str] = None
    is_group: bool = True


class ChatCreate(ChatBase):
    member_ids: List[int] = []


class ChatOut(ChatBase):
    id: int
    member_ids: List[int] = []

    class Config:
        orm_mode = True


class MessageBase(BaseModel):
    content: str


class MessageCreate(MessageBase):
    chat_id: Optional[int] = None
    sender_id: Optional[int] = None


class MessageOut(MessageBase):
    id: int
    chat_id: int
    sender_id: int
    created_at: datetime

    class Config:
        orm_mode = True
=======
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class MessageCreate(BaseModel):
    chat_id: int
    sender_id: int
    content: str


class Message(BaseModel):
    id: int
    chat_id: int
    sender_id: int
    content: str
    created_at: Optional[datetime]

    class Config:
        from_attributes = True


class ChatCreate(BaseModel):
    title: Optional[str] = None
    member_ids: List[int]


class Chat(BaseModel):
    id: int
    title: Optional[str]
    is_group: bool
    created_at: Optional[datetime]
    members: List[int] = []

    class Config:
        from_attributes = True
>>>>>>> main
