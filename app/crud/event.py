from sqlalchemy.orm import Session
from app.models.event import Event
from app.schemas.event import EventCreate
from typing import List, Optional


def get_event(db: Session, event_id: int) -> Optional[Event]:
    return db.query(Event).filter(Event.id == event_id).first()


def get_events(db: Session, skip: int = 0, limit: int = 100) -> List[Event]:
    return db.query(Event).offset(skip).limit(limit).all()


def create_event(db: Session, payload: EventCreate, created_by: Optional[int] = None) -> Event:
    e = Event(title=payload.title, description=payload.description, starts_at=payload.starts_at, created_by=created_by)
    db.add(e)
    db.commit()
    db.refresh(e)
    return e


def delete_event(db: Session, event_id: int) -> bool:
    e = get_event(db, event_id)
    if not e:
        return False
    db.delete(e)
    db.commit()
    return True
