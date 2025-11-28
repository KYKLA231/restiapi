<<<<<<< HEAD
from __future__ import annotations

import binascii
import hashlib
import os
from typing import Any, Dict, List, Optional

from sqlalchemy.orm import Session

from app.models.user import User
from app.schemas.user import UserCreate


PBKDF2_ITERATIONS = 100_000
PBKDF2_ALGO = "sha256"
SALT_SIZE_BYTES = 16


def _hash_password_raw(password: str, *, salt: Optional[bytes] = None) -> str:
    """
    Возвращает строку вида "<salt_hex>:<hash_hex>".
    """
    if salt is None:
        salt = os.urandom(SALT_SIZE_BYTES)

    dk = hashlib.pbkdf2_hmac(
        PBKDF2_ALGO,
        password.encode("utf-8"),
        salt,
        PBKDF2_ITERATIONS,
    )
    return f"{salt.hex()}:{dk.hex()}"


def _verify_password_raw(password: str, stored: str) -> bool:
    """
    Проверяет пароль по строке "<salt_hex>:<hash_hex>".
    """
    try:
        salt_hex, dk_hex = stored.split(":", 1)
    except ValueError:
        return False

    salt = bytes.fromhex(salt_hex)
    dk = hashlib.pbkdf2_hmac(
        PBKDF2_ALGO,
        password.encode("utf-8"),
        salt,
        PBKDF2_ITERATIONS,
    )
    return binascii.hexlify(dk).decode() == dk_hex


def get_user(db: Session, user_id: int) -> Optional[User]:
    return db.query(User).filter(User.id == user_id).first()


def get_user_by_email(db: Session, email: str) -> Optional[User]:
    return db.query(User).filter(User.email == email).first()


def get_users(db: Session, *, skip: int = 0, limit: int = 10) -> List[User]:
    return (
        db.query(User)
        .offset(skip)
        .limit(limit)
        .all()
    )


def create_user(db: Session, user: UserCreate) -> User:
    """
    Создаёт пользователя с захешированным паролем.
    """
    hashed_password = _hash_password_raw(user.password)

    db_user = User(
        name=user.name,
        email=user.email,
        hashed_password=hashed_password,
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user


def update_user(db: Session, user_id: int, user_data: Dict[str, Any]) -> Optional[User]:
    """
    Обновляет пользователя по словарю полей.
    Поле `password` конвертируется в `hashed_password`.
    """
    db_user = get_user(db, user_id)
    if not db_user:
        return None

    for key, value in user_data.items():
        if key == "password":
            value = _hash_password_raw(value)
            key = "hashed_password"

        if hasattr(db_user, key):
            setattr(db_user, key, value)

    db.commit()
    db.refresh(db_user)
    return db_user


def delete_user(db: Session, user_id: int) -> bool:
    db_user = get_user(db, user_id)
    if not db_user:
        return False

    db.delete(db_user)
    db.commit()
    return True


def add_friend(db: Session, user_id: int, friend_id: int) -> Optional[User]:
=======
from sqlalchemy.orm import Session
from sqlalchemy import or_
from app.models.user import User
from app.schemas.user import UserCreate
import hashlib
import os
import binascii

# Simple PBKDF2-HMAC-SHA256 helpers (avoid passlib/bcrypt issues on Windows)
def _hash_password_raw(password: str, salt: bytes = None) -> str:
    if salt is None:
        salt = os.urandom(16)
    dk = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
    return salt.hex() + ':' + dk.hex()

def _verify_password_raw(password: str, stored: str) -> bool:
    try:
        salt_hex, dk_hex = stored.split(':')
    except ValueError:
        return False
    salt = bytes.fromhex(salt_hex)
    dk = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
    return binascii.hexlify(dk).decode() == dk_hex

def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()

def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

def get_users(db: Session, skip: int = 0, limit: int = 10):
    return db.query(User).offset(skip).limit(limit).all()

def create_user(db: Session, user: UserCreate):
    # Hash password using PBKDF2-HMAC-SHA256 (no bcrypt, no 72-byte limit)
    hashed_password = _hash_password_raw(user.password)
    db_user = User(
        name=user.name,
        email=user.email,
        hashed_password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_user(db: Session, user_id: int, user_data: dict):
    db_user = get_user(db, user_id)
    if db_user:
        for key, value in user_data.items():
            if key == 'password':
                value = _hash_password_raw(value)
                key = 'hashed_password'
            setattr(db_user, key, value)
        db.commit()
        db.refresh(db_user)
    return db_user

def delete_user(db: Session, user_id: int):
    db_user = get_user(db, user_id)
    if db_user:
        db.delete(db_user)
        db.commit()
        return True
    return False


def add_friend(db: Session, user_id: int, friend_id: int):
>>>>>>> main
    user = get_user(db, user_id)
    friend = get_user(db, friend_id)
    if not user or not friend:
        return None
<<<<<<< HEAD

=======
    # avoid duplicate
>>>>>>> main
    if friend not in user.friends:
        user.friends.append(friend)
        db.commit()
        db.refresh(user)
<<<<<<< HEAD

    return user


def get_friends(db: Session, user_id: int) -> List[User]:
    user = get_user(db, user_id)
    if not user:
        return []
    return list(user.friends)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return _verify_password_raw(plain_password, hashed_password)


def authenticate_user(db: Session, email: str, password: str) -> Optional[User]:
    """
    Возвращает User при успешной аутентификации, иначе None.
    Не бросает исключений — это уровень CRUD.
    """
    if not email or not password:
        return None

    user = get_user_by_email(db, email)
    if not user:
        return None

    if not _verify_password_raw(password, user.hashed_password):
        return None

=======
    return user


def get_friends(db: Session, user_id: int):
    user = get_user(db, user_id)
    if not user:
        return []
    return user.friends

def verify_password(plain_password: str, hashed_password: str):
    return _verify_password_raw(plain_password, hashed_password)

def authenticate_user(db: Session, email: str, password: str):
    # guard against missing form/json fields — return False instead of raising
    if not email or not password:
        return False
    user = get_user_by_email(db, email)
    if not user:
        return False
    if not _verify_password_raw(password, user.hashed_password):
        return False
>>>>>>> main
    return user
