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
    prefix="/notifications",
    tags=["notifications"],
)


@router.get(
    "",
    response_model=List[schemas.NotificationOut],
)
def read_my_notifications(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
) -> List[schemas.NotificationOut]:
    return crud.notification.get_notifications_for_user(
        db,
        user_id=current_user.id,
        skip=skip,
        limit=limit,
    )


@router.post(
    "",
    response_model=schemas.NotificationOut,
    status_code=status.HTTP_201_CREATED,
)
def create_notification(
    payload: schemas.NotificationCreate,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
) -> schemas.NotificationOut:
    notification = crud.notification.create_notification(db, payload)
    return notification


@router.get(
    "/{notification_id}",
    response_model=schemas.NotificationOut,
)
def read_notification(
    notification_id: int,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
) -> schemas.NotificationOut:
    notification = crud.notification.get_notification(db, notification_id)
    if not notification:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Notification not found",
        )
    if notification.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not allowed to access this notification",
        )
    return notification


@router.post(
    "/{notification_id}/read",
    response_model=schemas.NotificationOut,
)
def mark_notification_read(
    notification_id: int,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
) -> schemas.NotificationOut:
    notification = crud.notification.get_notification(db, notification_id)
    if not notification:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Notification not found",
        )
    if notification.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not allowed to modify this notification",
        )

    updated = crud.notification.mark_read(db, notification_id)
    return updated


@router.delete(
    "/{notification_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_notification(
    notification_id: int,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
) -> None:
    notification = crud.notification.get_notification(db, notification_id)
    if not notification:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Notification not found",
        )
    if notification.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not allowed to delete this notification",
        )

    crud.notification.delete_notification(db, notification_id)
=======
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
>>>>>>> main
