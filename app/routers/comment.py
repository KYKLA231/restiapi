from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.comment import CommentCreate, CommentInDB
from app.crud import comment as comment_crud

router = APIRouter(prefix="/api/comments", tags=["comments"])


@router.post('/', response_model=CommentInDB)
def create_comment(payload: CommentCreate, db: Session = Depends(get_db)):
    return comment_crud.create_comment(db, payload)


@router.get('/post/{post_id}', response_model=List[CommentInDB])
def list_comments_for_post(post_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return comment_crud.get_comments_for_post(db, post_id, skip=skip, limit=limit)


@router.delete('/{comment_id}')
def delete_comment(comment_id: int, db: Session = Depends(get_db)):
    ok = comment_crud.delete_comment(db, comment_id)
    if not ok:
        raise HTTPException(status_code=404, detail='Comment not found')
    return {"deleted": True}
