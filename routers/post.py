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
    prefix="/posts",
    tags=["posts"],
)


@router.post(
    "",
    response_model=schemas.PostOut,
    status_code=status.HTTP_201_CREATED,
)
def create_post(
    payload: schemas.PostCreate,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
) -> schemas.PostOut:
    post = crud.post.create_post(db, payload, owner_id=current_user.id)
    return post


@router.get(
    "",
    response_model=List[schemas.PostOut],
)
def read_posts(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
) -> List[schemas.PostOut]:
    return crud.post.get_posts(db, skip=skip, limit=limit)


@router.get(
    "/{post_id}",
    response_model=schemas.PostOut,
)
def read_post(
    post_id: int,
    db: Session = Depends(get_db),
) -> schemas.PostOut:
    post = crud.post.get_post(db, post_id)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found",
        )
    return post


@router.put(
    "/{post_id}",
    response_model=schemas.PostOut,
)
def update_post(
    post_id: int,
    payload: schemas.PostUpdate,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
) -> schemas.PostOut:
    post = crud.post.get_post(db, post_id)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found",
        )

    if post.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not allowed to update this post",
        )

    updated = crud.post.update_post(db, post_id, payload)
    return updated


@router.delete(
    "/{post_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_post(
    post_id: int,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
) -> None:
    post = crud.post.get_post(db, post_id)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found",
        )

    if post.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not allowed to delete this post",
        )

    crud.post.delete_post(db, post_id)
=======
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
>>>>>>> main
