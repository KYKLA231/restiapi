from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, DateTime, Table
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base


# Many-to-many between chats and users (members)
chat_members = Table(
    'chat_members',
    Base.metadata,
    Column('chat_id', Integer, ForeignKey('chats.id'), primary_key=True),
    Column('user_id', Integer, ForeignKey('users.id'), primary_key=True),
)


class Chat(Base):
    __tablename__ = 'chats'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=True)
    is_group = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    members = relationship('app.models.user.User', secondary=chat_members, backref='chats')
    messages = relationship('Message', back_populates='chat', cascade='all, delete-orphan')


class Message(Base):
    __tablename__ = 'messages'

    id = Column(Integer, primary_key=True, index=True)
    chat_id = Column(Integer, ForeignKey('chats.id'))
    sender_id = Column(Integer, ForeignKey('users.id'))
    content = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

    chat = relationship('Chat', back_populates='messages')
    sender = relationship('app.models.user.User')
