from sqlalchemy.orm import Session
from app.models.notification import Notification
from app.schemas.notification import NotificationCreate
from typing import List, Optional


def get_notification(db: Session, notification_id: int) -> Optional[Notification]:
    return db.query(Notification).filter(Notification.id == notification_id).first()


def get_notifications_for_user(db: Session, user_id: int, skip: int = 0, limit: int = 100) -> List[Notification]:
    return db.query(Notification).filter(Notification.user_id == user_id).offset(skip).limit(limit).all()


def create_notification(db: Session, payload: NotificationCreate) -> Notification:
    n = Notification(user_id=payload.user_id, message=payload.message)
    db.add(n)
    db.commit()
    db.refresh(n)
    return n


def mark_read(db: Session, notification_id: int) -> Optional[Notification]:
    n = get_notification(db, notification_id)
    if not n:
        return None
    n.read = True
    db.commit()
    db.refresh(n)
    return n


def delete_notification(db: Session, notification_id: int) -> bool:
    n = get_notification(db, notification_id)
    if not n:
        return False
    db.delete(n)
    db.commit()
    return True
