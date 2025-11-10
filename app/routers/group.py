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
