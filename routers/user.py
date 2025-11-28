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
    prefix="/users",
    tags=["users"],
)


@router.post(
    "",
    response_model=schemas.UserOut,
    status_code=status.HTTP_201_CREATED,
)
def create_user(
    payload: schemas.UserCreate,
    db: Session = Depends(get_db),
) -> schemas.UserOut:
    existing = crud.user.get_user_by_email(db, payload.email)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )
    user = crud.user.create_user(db, payload)
    return user


@router.get(
    "/me",
    response_model=schemas.UserOut,
)
def read_current_user(
    current_user: UserModel = Depends(get_current_user),
) -> schemas.UserOut:
    return current_user


@router.get(
    "/{user_id}",
    response_model=schemas.UserOut,
)
def read_user(
    user_id: int,
    db: Session = Depends(get_db),
) -> schemas.UserOut:
    user = crud.user.get_user(db, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    return user


@router.get(
    "",
    response_model=List[schemas.UserOut],
)
def read_users(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db),
) -> List[schemas.UserOut]:
    return crud.user.get_users(db, skip=skip, limit=limit)


@router.put(
    "/{user_id}",
    response_model=schemas.UserOut,
)
def update_user(
    user_id: int,
    payload: schemas.UserUpdate,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
) -> schemas.UserOut:
    if current_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not allowed to update this user",
        )

    updated = crud.user.update_user(db, user_id, payload.dict(exclude_unset=True))
    if not updated:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    return updated


@router.delete(
    "/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
) -> None:
    if current_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not allowed to delete this user",
        )
    ok = crud.user.delete_user(db, user_id)
    if not ok:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )


@router.post(
    "/{user_id}/friends/{friend_id}",
    response_model=schemas.UserOut,
)
def add_friend(
    user_id: int,
    friend_id: int,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
) -> schemas.UserOut:
    if current_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not allowed to modify friends for this user",
        )

    user = crud.user.add_friend(db, user_id, friend_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User or friend not found",
        )
    return user


@router.get(
    "/{user_id}/friends",
    response_model=List[schemas.UserOut],
)
def get_friends(
    user_id: int,
    db: Session = Depends(get_db),
) -> List[schemas.UserOut]:
    return crud.user.get_friends(db, user_id)
=======
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import Dict, Any
from app import crud, database
from app.schemas import user as schemas
from app.auth import create_access_token, get_current_user

router = APIRouter(
    prefix="/api/users",
    tags=["users"]
)

@router.post("/register")
def create_user(user: schemas.UserCreate, db: Session = Depends(database.get_db)):
    db_user = crud.user.get_user_by_email(db, user.email)
    if db_user:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )
    new_user = crud.user.create_user(db, user)
    # issue access token immediately so client can use it to authenticate right after registration
    access_token = create_access_token(data={"sub": new_user.email})
    return {"user": new_user, "access_token": access_token, "token_type": "bearer"}

@router.post("/token")
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    user = crud.user.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me", response_model=schemas.User)
def read_users_me(current_user = Depends(get_current_user)):
    return current_user

@router.get("/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(database.get_db)):
    db_user = crud.user.get_user(db, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@router.get("/", response_model=list[schemas.User])
def read_users(skip: int = 0, limit: int = 10, db: Session = Depends(database.get_db)):
    return crud.user.get_users(db, skip=skip, limit=limit)

@router.put("/{user_id}", response_model=schemas.User)
def update_user(
    user_id: int,
    user_data: Dict[str, Any],
    db: Session = Depends(database.get_db)
):
    updated_user = crud.user.update_user(db, user_id, user_data)
    if not updated_user:
        raise HTTPException(status_code=404, detail="User not found")
    return updated_user

@router.delete("/{user_id}")
def delete_user(user_id: int, db: Session = Depends(database.get_db)):
    success = crud.user.delete_user(db, user_id)
    if not success:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deleted successfully"}


@router.put("/me", response_model=schemas.User)
def update_me(user_update: schemas.UserUpdate, current_user = Depends(get_current_user), db: Session = Depends(database.get_db)):
    data = user_update.dict(exclude_none=True)
    updated = crud.user.update_user(db, current_user.id, data)
    if not updated:
        raise HTTPException(status_code=404, detail="User not found")
    return updated


@router.post("/me/friends/{friend_id}", response_model=schemas.User)
def add_friend_endpoint(friend_id: int, current_user = Depends(get_current_user), db: Session = Depends(database.get_db)):
    added = crud.user.add_friend(db, current_user.id, friend_id)
    if not added:
        raise HTTPException(status_code=404, detail="User or friend not found")
    return added


@router.get("/me/friends", response_model=list[schemas.User])
def list_friends(current_user = Depends(get_current_user), db: Session = Depends(database.get_db)):
    friends = crud.user.get_friends(db, current_user.id)
    return friends
>>>>>>> main
