from sqlalchemy.orm import Session
from app.models.comment import Comment
from app.schemas.comment import CommentCreate
from typing import List, Optional


def get_comment(db: Session, comment_id: int) -> Optional[Comment]:
    return db.query(Comment).filter(Comment.id == comment_id).first()


def get_comments_for_post(db: Session, post_id: int, skip: int = 0, limit: int = 100) -> List[Comment]:
    return db.query(Comment).filter(Comment.post_id == post_id).offset(skip).limit(limit).all()


def create_comment(db: Session, payload: CommentCreate, author_id: Optional[int] = None) -> Comment:
    c = Comment(content=payload.content, post_id=payload.post_id, author_id=author_id)
    db.add(c)
    db.commit()
    db.refresh(c)
    return c


def delete_comment(db: Session, comment_id: int) -> bool:
    c = get_comment(db, comment_id)
    if not c:
        return False
    db.delete(c)
    db.commit()
    return True
