<<<<<<< HEAD
from __future__ import annotations

from typing import List, Optional

from sqlalchemy.orm import Session

from app.models.group import Group
from app.models.user import User
from app.schemas.group import GroupCreate, GroupUpdate
=======
from sqlalchemy.orm import Session
from app.models.group import Group
from app.schemas.group import GroupCreate, GroupUpdate
from typing import List, Optional
>>>>>>> main


def get_group(db: Session, group_id: int) -> Optional[Group]:
    return db.query(Group).filter(Group.id == group_id).first()


<<<<<<< HEAD
def get_groups(
    db: Session,
    *,
    skip: int = 0,
    limit: int = 100,
) -> List[Group]:
    return (
        db.query(Group)
        .offset(skip)
        .limit(limit)
        .all()
    )


def create_group(db: Session, payload: GroupCreate) -> Group:
    group = Group(
        name=payload.name,
        description=payload.description,
    )

    db.add(group)
    db.commit()
    db.refresh(group)

    return group


def update_group(
    db: Session,
    group_id: int,
    patch: GroupUpdate,
) -> Optional[Group]:
    group = get_group(db, group_id)
    if not group:
        return None

    if patch.name is not None:
        group.name = patch.name
    if patch.description is not None:
        group.description = patch.description

    db.commit()
    db.refresh(group)
    return group


def delete_group(db: Session, group_id: int) -> bool:
    group = get_group(db, group_id)
    if not group:
        return False

    db.delete(group)
=======
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
>>>>>>> main
    db.commit()
    return True


<<<<<<< HEAD
def add_member(db: Session, group: Group, user: User) -> Group:
    """
    Добавляет участника в группу, если его ещё нет.
    """
=======
def add_member(db: Session, group: Group, user):
>>>>>>> main
    if user not in group.members:
        group.members.append(user)
        db.commit()
        db.refresh(group)
    return group


<<<<<<< HEAD
def remove_member(db: Session, group: Group, user: User) -> Group:
    """
    Удаляет участника из группы, если он там есть.
    """
=======
def remove_member(db: Session, group: Group, user):
>>>>>>> main
    if user in group.members:
        group.members.remove(user)
        db.commit()
        db.refresh(group)
    return group
