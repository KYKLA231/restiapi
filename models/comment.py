<<<<<<< HEAD
from __future__ import annotations

from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, Text
from sqlalchemy.orm import Mapped, relationship

=======
from sqlalchemy import Column, Integer, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
>>>>>>> main
from app.database import Base


class Comment(Base):
<<<<<<< HEAD
    __tablename__ = "comments"

    id: Mapped[int] = Column(Integer, primary_key=True, index=True)
    content: Mapped[str] = Column(Text, nullable=False)
    post_id: Mapped[int] = Column(Integer, ForeignKey("posts.id"), nullable=False)
    author_id: Mapped[int | None] = Column(Integer, ForeignKey("users.id"), nullable=True)
    created_at: Mapped[datetime] = Column(DateTime, default=datetime.utcnow)

    post = relationship("Post", back_populates="comments")
    author = relationship("User")
=======
    __tablename__ = 'comments'
    id = Column(Integer, primary_key=True, index=True)
    content = Column(Text, nullable=False)
    post_id = Column(Integer, ForeignKey('posts.id'), nullable=False)
    author_id = Column(Integer, ForeignKey('users.id'), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    post = relationship('Post', back_populates='comments')
    author = relationship('User')
>>>>>>> main
