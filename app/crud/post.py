from sqlalchemy.orm import Session
from app.models.post import Post
from app.schemas.post import PostCreate, PostUpdate
from typing import List, Optional


def get_post(db: Session, post_id: int) -> Optional[Post]:
    return db.query(Post).filter(Post.id == post_id).first()


def get_posts(db: Session, skip: int = 0, limit: int = 100) -> List[Post]:
    return db.query(Post).offset(skip).limit(limit).all()


def create_post(db: Session, post: PostCreate, owner_id: Optional[int] = None) -> Post:
    db_post = Post(title=post.title, content=post.content, owner_id=owner_id)
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post


def update_post(db: Session, post_id: int, patch: PostUpdate) -> Optional[Post]:
    db_post = get_post(db, post_id)
    if not db_post:
        return None
    if patch.title is not None:
        db_post.title = patch.title
    if patch.content is not None:
        db_post.content = patch.content
    db.commit()
    db.refresh(db_post)
    return db_post


def delete_post(db: Session, post_id: int) -> bool:
    db_post = get_post(db, post_id)
    if not db_post:
        return False
    db.delete(db_post)
    db.commit()
    return True
