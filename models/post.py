<<<<<<< HEAD
from __future__ import annotations

from datetime import datetime
from typing import List

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, relationship

=======
from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
>>>>>>> main
from app.database import Base


class Post(Base):
<<<<<<< HEAD
    __tablename__ = "posts"

    id: Mapped[int] = Column(Integer, primary_key=True, index=True)
    title: Mapped[str] = Column(String(200), nullable=False)
    content: Mapped[str | None] = Column(Text, nullable=True)
    owner_id: Mapped[int | None] = Column(Integer, ForeignKey("users.id"), nullable=True)
    created_at: Mapped[datetime] = Column(DateTime, default=datetime.utcnow)

    owner = relationship("User", back_populates="posts")
    comments: Mapped[List["Comment"]] = relationship(
        "Comment",
        back_populates="post",
        cascade="all, delete-orphan",
    )
=======
    __tablename__ = 'posts'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    content = Column(Text, nullable=True)
    owner_id = Column(Integer, ForeignKey('users.id'), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    owner = relationship('User', back_populates='posts')
    # comments on this post (back_populates from Comment.post)
    comments = relationship('Comment', back_populates='post')
>>>>>>> main
