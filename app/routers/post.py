from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.post import PostCreate, PostInDB, PostUpdate
from app.crud import post as post_crud

router = APIRouter(prefix="/api/posts", tags=["posts"])


@router.post('/', response_model=PostInDB)
def create_post(payload: PostCreate, db: Session = Depends(get_db)):
    return post_crud.create_post(db, payload)


@router.get('/', response_model=List[PostInDB])
def list_posts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return post_crud.get_posts(db, skip=skip, limit=limit)


@router.get('/{post_id}', response_model=PostInDB)
def read_post(post_id: int, db: Session = Depends(get_db)):
    p = post_crud.get_post(db, post_id)
    if not p:
        raise HTTPException(status_code=404, detail='Post not found')
    return p


@router.put('/{post_id}', response_model=PostInDB)
def update_post(post_id: int, patch: PostUpdate, db: Session = Depends(get_db)):
    p = post_crud.update_post(db, post_id, patch)
    if not p:
        raise HTTPException(status_code=404, detail='Post not found')
    return p


@router.delete('/{post_id}')
def delete_post(post_id: int, db: Session = Depends(get_db)):
    ok = post_crud.delete_post(db, post_id)
    if not ok:
        raise HTTPException(status_code=404, detail='Post not found')
    return {"deleted": True}
