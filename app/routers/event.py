from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.event import EventCreate, EventInDB
from app.crud import event as event_crud

router = APIRouter(prefix="/api/events", tags=["events"])


@router.post('/', response_model=EventInDB)
def create_event(payload: EventCreate, db: Session = Depends(get_db)):
    return event_crud.create_event(db, payload)


@router.get('/', response_model=List[EventInDB])
def list_events(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return event_crud.get_events(db, skip=skip, limit=limit)


@router.delete('/{event_id}')
def delete_event(event_id: int, db: Session = Depends(get_db)):
    ok = event_crud.delete_event(db, event_id)
    if not ok:
        raise HTTPException(status_code=404, detail='Event not found')
    return {"deleted": True}
