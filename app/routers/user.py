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
