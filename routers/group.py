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
    prefix="/groups",
    tags=["groups"],
)


@router.post(
    "",
    response_model=schemas.GroupOut,
    status_code=status.HTTP_201_CREATED,
)
def create_group(
    payload: schemas.GroupCreate,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
) -> schemas.GroupOut:
    group = crud.group.create_group(db, payload)
    return group


@router.get(
    "",
    response_model=List[schemas.GroupOut],
)
def read_groups(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
) -> List[schemas.GroupOut]:
    return crud.group.get_groups(db, skip=skip, limit=limit)


@router.get(
    "/{group_id}",
    response_model=schemas.GroupOut,
)
def read_group(
    group_id: int,
    db: Session = Depends(get_db),
) -> schemas.GroupOut:
    group = crud.group.get_group(db, group_id)
    if not group:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Group not found",
        )
    return group


@router.put(
    "/{group_id}",
    response_model=schemas.GroupOut,
)
def update_group(
    group_id: int,
    payload: schemas.GroupUpdate,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
) -> schemas.GroupOut:
    group = crud.group.update_group(db, group_id, payload)
    if not group:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Group not found",
        )
    return group


@router.delete(
    "/{group_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_group(
    group_id: int,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
) -> None:
    ok = crud.group.delete_group(db, group_id)
    if not ok:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Group not found",
        )


@router.post(
    "/{group_id}/join",
    response_model=schemas.GroupOut,
)
def join_group(
    group_id: int,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
) -> schemas.GroupOut:
    group = crud.group.get_group(db, group_id)
    if not group:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Group not found",
        )

    updated = crud.group.add_member(db, group, current_user)
    return updated


@router.post(
    "/{group_id}/leave",
    response_model=schemas.GroupOut,
)
def leave_group(
    group_id: int,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
) -> schemas.GroupOut:
    group = crud.group.get_group(db, group_id)
    if not group:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Group not found",
        )

    updated = crud.group.remove_member(db, group, current_user)
    return updated
=======
from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.group import GroupCreate, GroupInDB, GroupUpdate
from app.crud import group as group_crud
from app.crud import user as user_crud

router = APIRouter(prefix="/api/groups", tags=["groups"])


@router.post('/', response_model=GroupInDB)
def create_group(payload: GroupCreate, db: Session = Depends(get_db)):
    return group_crud.create_group(db, payload)


@router.get('/', response_model=List[GroupInDB])
def list_groups(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return group_crud.get_groups(db, skip=skip, limit=limit)


@router.get('/{group_id}', response_model=GroupInDB)
def read_group(group_id: int, db: Session = Depends(get_db)):
    g = group_crud.get_group(db, group_id)
    if not g:
        raise HTTPException(status_code=404, detail='Group not found')
    return g


@router.post('/{group_id}/members/{user_id}', response_model=GroupInDB)
def add_member(group_id: int, user_id: int, db: Session = Depends(get_db)):
    g = group_crud.get_group(db, group_id)
    if not g:
        raise HTTPException(status_code=404, detail='Group not found')
    u = user_crud.get_user(db, user_id)
    if not u:
        raise HTTPException(status_code=404, detail='User not found')
    g = group_crud.add_member(db, g, u)
    return g


@router.delete('/{group_id}/members/{user_id}', response_model=GroupInDB)
def remove_member(group_id: int, user_id: int, db: Session = Depends(get_db)):
    g = group_crud.get_group(db, group_id)
    if not g:
        raise HTTPException(status_code=404, detail='Group not found')
    u = user_crud.get_user(db, user_id)
    if not u:
        raise HTTPException(status_code=404, detail='User not found')
    g = group_crud.remove_member(db, g, u)
    return g


@router.put('/{group_id}', response_model=GroupInDB)
def update_group(group_id: int, patch: GroupUpdate, db: Session = Depends(get_db)):
    g = group_crud.update_group(db, group_id, patch)
    if not g:
        raise HTTPException(status_code=404, detail='Group not found')
    return g


@router.delete('/{group_id}')
def delete_group(group_id: int, db: Session = Depends(get_db)):
    ok = group_crud.delete_group(db, group_id)
    if not ok:
        raise HTTPException(status_code=404, detail='Group not found')
    return {"deleted": True}
>>>>>>> main
