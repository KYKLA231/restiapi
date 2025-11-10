from sqlalchemy.orm import Session
from app.models.group import Group
from app.schemas.group import GroupCreate, GroupUpdate
from typing import List, Optional


def get_group(db: Session, group_id: int) -> Optional[Group]:
    return db.query(Group).filter(Group.id == group_id).first()


def get_groups(db: Session, skip: int = 0, limit: int = 100) -> List[Group]:
    return db.query(Group).offset(skip).limit(limit).all()


def create_group(db: Session, group: GroupCreate) -> Group:
    db_group = Group(name=group.name, description=group.description)
    db.add(db_group)
    db.commit()
    db.refresh(db_group)
    return db_group


def update_group(db: Session, group_id: int, patch: GroupUpdate) -> Optional[Group]:
    db_group = get_group(db, group_id)
    if not db_group:
        return None
    if patch.name is not None:
        db_group.name = patch.name
    if patch.description is not None:
        db_group.description = patch.description
    db.commit()
    db.refresh(db_group)
    return db_group


def delete_group(db: Session, group_id: int) -> bool:
    db_group = get_group(db, group_id)
    if not db_group:
        return False
    db.delete(db_group)
    db.commit()
    return True


def add_member(db: Session, group: Group, user):
    if user not in group.members:
        group.members.append(user)
        db.commit()
        db.refresh(group)
    return group


def remove_member(db: Session, group: Group, user):
    if user in group.members:
        group.members.remove(user)
        db.commit()
        db.refresh(group)
    return group
