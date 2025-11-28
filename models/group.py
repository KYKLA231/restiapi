<<<<<<< HEAD
from __future__ import annotations

from typing import List

from sqlalchemy import Column, ForeignKey, Integer, String, Table, Text
from sqlalchemy.orm import Mapped, relationship

=======
from sqlalchemy import Column, Integer, String, Text, Table, ForeignKey
from sqlalchemy.orm import relationship
>>>>>>> main
from app.database import Base


group_members = Table(
<<<<<<< HEAD
    "group_members",
    Base.metadata,
    Column("group_id", Integer, ForeignKey("groups.id"), primary_key=True),
    Column("user_id", Integer, ForeignKey("users.id"), primary_key=True),
=======
    'group_members', Base.metadata,
    Column('group_id', Integer, ForeignKey('groups.id'), primary_key=True),
    Column('user_id', Integer, ForeignKey('users.id'), primary_key=True),
>>>>>>> main
)


class Group(Base):
<<<<<<< HEAD
    __tablename__ = "groups"

    id: Mapped[int] = Column(Integer, primary_key=True, index=True)
    name: Mapped[str] = Column(String(150), unique=True, nullable=False)
    description: Mapped[str | None] = Column(Text, nullable=True)

    members: Mapped[List["User"]] = relationship(
        "User",
        secondary=group_members,
        back_populates="groups",
    )
=======
    __tablename__ = 'groups'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(150), unique=True, nullable=False)
    description = Column(Text, nullable=True)

    members = relationship('User', secondary=group_members, back_populates='groups')
>>>>>>> main
