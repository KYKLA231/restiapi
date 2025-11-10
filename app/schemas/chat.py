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
