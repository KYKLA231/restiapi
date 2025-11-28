<<<<<<< HEAD
from __future__ import annotations

from typing import List, Optional

from pydantic import BaseModel, EmailStr

from pydantic import BaseModel

class Token(BaseModel):
    access_token: str
    token_type: str

=======
from pydantic import BaseModel, EmailStr
from typing import Optional
>>>>>>> main

class UserBase(BaseModel):
    name: str
    email: EmailStr
    avatar: Optional[str] = None
    bio: Optional[str] = None

<<<<<<< HEAD

class UserCreate(UserBase):
    password: str


class UserUpdate(BaseModel):
    name: Optional[str] = None
    avatar: Optional[str] = None
    bio: Optional[str] = None
    password: Optional[str] = None


class UserOut(UserBase):
    id: int
    is_active: bool

    class Config:
        orm_mode = True


class FriendOut(UserOut):
    pass
=======
class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    is_active: bool
    friends: Optional[list[int]] = []

    class Config:
        from_attributes = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserUpdate(BaseModel):
    name: Optional[str] = None
    password: Optional[str] = None
    avatar: Optional[str] = None
    bio: Optional[str] = None
>>>>>>> main
