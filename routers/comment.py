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
    prefix="/comments",
    tags=["comments"],
)


@router.post(
    "",
    response_model=schemas.CommentOut,
    status_code=status.HTTP_201_CREATED,
)
def create_comment(
    payload: schemas.CommentCreate,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
) -> schemas.CommentOut:
    comment = crud.comment.create_comment(
        db,
        payload,
        author_id=current_user.id,
    )
    return comment


@router.get(
    "/post/{post_id}",
    response_model=List[schemas.CommentOut],
)
def read_comments_for_post(
    post_id: int,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
) -> List[schemas.CommentOut]:
    return crud.comment.get_comments_for_post(
        db,
        post_id=post_id,
        skip=skip,
        limit=limit,
    )


@router.get(
    "/{comment_id}",
    response_model=schemas.CommentOut,
)
def read_comment(
    comment_id: int,
    db: Session = Depends(get_db),
) -> schemas.CommentOut:
    comment = crud.comment.get_comment(db, comment_id)
    if not comment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Comment not found",
        )
    return comment


@router.delete(
    "/{comment_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_comment(
    comment_id: int,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
) -> None:
    comment = crud.comment.get_comment(db, comment_id)
    if not comment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Comment not found",
        )

    if comment.author_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not allowed to delete this comment",
        )

    crud.comment.delete_comment(db, comment_id)
=======
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
>>>>>>> main
