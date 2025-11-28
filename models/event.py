<<<<<<< HEAD
from __future__ import annotations

from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, relationship

=======
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
>>>>>>> main
from app.database import Base


class Event(Base):
<<<<<<< HEAD
    __tablename__ = "events"

    id: Mapped[int] = Column(Integer, primary_key=True, index=True)
    title: Mapped[str] = Column(String(200), nullable=False)
    description: Mapped[str | None] = Column(Text, nullable=True)
    starts_at: Mapped[datetime | None] = Column(DateTime, nullable=True)
    created_by: Mapped[int | None] = Column(Integer, ForeignKey("users.id"), nullable=True)
    created_at: Mapped[datetime] = Column(DateTime, default=datetime.utcnow)

    creator = relationship("User")
=======
    __tablename__ = 'events'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    starts_at = Column(DateTime, nullable=True)
    created_by = Column(Integer, ForeignKey('users.id'), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    creator = relationship('User')
>>>>>>> main
