<<<<<<< HEAD
from __future__ import annotations

from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import crud, schemas
from app.database import get_db
from app.auth import get_current_user
from app.models.user import User as UserModel

router = APIRouter(
    prefix="/events",
    tags=["events"],
)


@router.post(
    "",
    response_model=schemas.EventOut,
    status_code=status.HTTP_201_CREATED,
)
def create_event(
    payload: schemas.EventCreate,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
) -> schemas.EventOut:
    event = crud.event.create_event(
        db,
        payload,
        created_by=current_user.id,
    )
    return event


@router.get(
    "",
    response_model=List[schemas.EventOut],
)
def read_events(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
) -> List[schemas.EventOut]:
    return crud.event.get_events(db, skip=skip, limit=limit)


@router.get(
    "/{event_id}",
    response_model=schemas.EventOut,
)
def read_event(
    event_id: int,
    db: Session = Depends(get_db),
) -> schemas.EventOut:
    event = crud.event.get_event(db, event_id)
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event not found",
        )
    return event


@router.delete(
    "/{event_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_event(
    event_id: int,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
) -> None:
    event = crud.event.get_event(db, event_id)
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event not found",
        )

    if event.created_by and event.created_by != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not allowed to delete this event",
        )

    crud.event.delete_event(db, event_id)
=======
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
>>>>>>> main
