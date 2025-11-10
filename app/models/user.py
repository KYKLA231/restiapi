from sqlalchemy import Column, Integer, String, Boolean
from app.database import Base
from sqlalchemy import Table, ForeignKey
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    avatar = Column(String, nullable=True)
    bio = Column(String, nullable=True)

# association table for friendships (symmetric)
friends_association = Table(
    'friends',
    Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id'), primary_key=True),
    Column('friend_id', Integer, ForeignKey('users.id'), primary_key=True)
)

# backref relationship added dynamically in user mapping
User.friends = relationship(
    'User',
    secondary=friends_association,
    primaryjoin=User.id == friends_association.c.user_id,
    secondaryjoin=User.id == friends_association.c.friend_id,
    backref='friend_of'
)

# posts authored by the user
User.posts = relationship('Post', back_populates='owner')

# groups membership (secondary table is defined in app.models.group as 'group_members')
User.groups = relationship('Group', secondary='group_members', back_populates='members')
