from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.notification import NotificationCreate, NotificationInDB
from app.crud import notification as notification_crud

router = APIRouter(prefix="/api/notifications", tags=["notifications"])


@router.post('/', response_model=NotificationInDB)
def create_notification(payload: NotificationCreate, db: Session = Depends(get_db)):
    return notification_crud.create_notification(db, payload)


@router.get('/user/{user_id}', response_model=List[NotificationInDB])
def list_notifications(user_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return notification_crud.get_notifications_for_user(db, user_id, skip=skip, limit=limit)


@router.post('/{notification_id}/read', response_model=NotificationInDB)
def mark_read(notification_id: int, db: Session = Depends(get_db)):
    n = notification_crud.mark_read(db, notification_id)
    if not n:
        raise HTTPException(status_code=404, detail='Notification not found')
    return n


@router.delete('/{notification_id}')
def delete_notification(notification_id: int, db: Session = Depends(get_db)):
    ok = notification_crud.delete_notification(db, notification_id)
    if not ok:
        raise HTTPException(status_code=404, detail='Notification not found')
    return {"deleted": True}
