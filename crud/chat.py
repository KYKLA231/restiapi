<<<<<<< HEAD
from __future__ import annotations

from typing import List, Optional

from sqlalchemy.orm import Session

from app.models.chat import Chat, Message
from app.models.user import User
from app.schemas.chat import ChatCreate, MessageCreate


def create_chat(db: Session, chat_in: ChatCreate) -> Chat:
    """
    Создаёт групповой чат и привязывает участников.
    """
    chat = Chat(
        title=chat_in.title,
        is_group=True,
    )

    if chat_in.member_ids:
        members = (
            db.query(User)
            .filter(User.id.in_(chat_in.member_ids))
            .all()
        )
        chat.members = members

    db.add(chat)
    db.commit()
    db.refresh(chat)

    return chat


def get_chat(db: Session, chat_id: int) -> Optional[Chat]:
    return db.query(Chat).filter(Chat.id == chat_id).first()


def post_message(db: Session, msg_in: MessageCreate) -> Optional[Message]:
    """
    Создаёт сообщение в чате, если существуют чат и отправитель.
    """
    chat = get_chat(db, msg_in.chat_id)
    if not chat:
        return None

    sender = db.query(User).filter(User.id == msg_in.sender_id).first()
    if not sender:
        return None

    message = Message(
        chat_id=chat.id,
        sender_id=sender.id,
        content=msg_in.content,
    )

    db.add(message)
    db.commit()
    db.refresh(message)

    return message


def get_messages(
    db: Session,
    chat_id: int,
    *,
    limit: int = 50,
) -> List[Message]:
    chat = get_chat(db, chat_id)
    if not chat:
        return []

    return (
        db.query(Message)
        .filter(Message.chat_id == chat_id)
        .order_by(Message.created_at)
        .limit(limit)
        .all()
    )
=======
from sqlalchemy.orm import Session
from app.models.chat import Chat, Message
from app.models.user import User
from app.schemas.chat import ChatCreate, MessageCreate
from typing import List


def create_chat(db: Session, chat_in: ChatCreate):
    chat = Chat(title=chat_in.title, is_group=True)
    # attach members
    members = db.query(User).filter(User.id.in_(chat_in.member_ids)).all()
    chat.members = members
    db.add(chat)
    db.commit()
    db.refresh(chat)
    return chat


def get_chat(db: Session, chat_id: int):
    return db.query(Chat).filter(Chat.id == chat_id).first()


def post_message(db: Session, msg_in: MessageCreate):
    chat = get_chat(db, msg_in.chat_id)
    sender = db.query(User).filter(User.id == msg_in.sender_id).first()
    if not chat or not sender:
        return None
    message = Message(chat_id=chat.id, sender_id=sender.id, content=msg_in.content)
    db.add(message)
    db.commit()
    db.refresh(message)
    return message


def get_messages(db: Session, chat_id: int, limit: int = 50):
    chat = get_chat(db, chat_id)
    if not chat:
        return []
    return db.query(Message).filter(Message.chat_id == chat_id).order_by(Message.created_at).limit(limit).all()
>>>>>>> main
