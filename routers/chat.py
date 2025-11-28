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
    prefix="/chats",
    tags=["chats"],
)


@router.post(
    "",
    response_model=schemas.ChatOut,
    status_code=status.HTTP_201_CREATED,
)
def create_chat(
    payload: schemas.ChatCreate,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
) -> schemas.ChatOut:
    member_ids = set(payload.member_ids or [])
    member_ids.add(current_user.id)
    payload.member_ids = list(member_ids)

    chat = crud.chat.create_chat(db, payload)
    return chat


@router.get(
    "/{chat_id}",
    response_model=schemas.ChatOut,
)
def read_chat(
    chat_id: int,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
) -> schemas.ChatOut:
    chat = crud.chat.get_chat(db, chat_id)
    if not chat:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Chat not found",
        )
    return chat


@router.get(
    "/{chat_id}/messages",
    response_model=List[schemas.MessageOut],
)
def read_messages(
    chat_id: int,
    limit: int = 50,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
) -> List[schemas.MessageOut]:
    messages = crud.chat.get_messages(db, chat_id, limit=limit)
    if messages == []:
        chat = crud.chat.get_chat(db, chat_id)
        if not chat:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Chat not found",
            )
    return messages


@router.post(
    "/{chat_id}/messages",
    response_model=schemas.MessageOut,
    status_code=status.HTTP_201_CREATED,
)
def send_message(
    chat_id: int,
    payload: schemas.MessageCreate,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
) -> schemas.MessageOut:
    payload.chat_id = chat_id
    payload.sender_id = current_user.id

    message = crud.chat.post_message(db, payload)
    if not message:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Chat or sender not found",
        )
    return message
=======
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import crud, database
from app.schemas import chat as schemas

router = APIRouter(
    prefix="/api/chats",
    tags=["chats"]
)


@router.post("/", response_model=schemas.Chat)
def create_chat(chat_in: schemas.ChatCreate, db: Session = Depends(database.get_db)):
    chat = crud.chat.create_chat(db, chat_in)
    return chat


@router.get("/{chat_id}", response_model=schemas.Chat)
def read_chat(chat_id: int, db: Session = Depends(database.get_db)):
    chat = crud.chat.get_chat(db, chat_id)
    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found")
    return chat


@router.post("/{chat_id}/messages", response_model=schemas.Message)
def post_message(chat_id: int, msg: schemas.MessageCreate, db: Session = Depends(database.get_db)):
    if msg.chat_id != chat_id:
        raise HTTPException(status_code=400, detail="chat_id mismatch")
    message = crud.chat.post_message(db, msg)
    if not message:
        raise HTTPException(status_code=400, detail="Unable to post message")
    return message


@router.get("/{chat_id}/messages", response_model=list[schemas.Message])
def list_messages(chat_id: int, db: Session = Depends(database.get_db)):
    return crud.chat.get_messages(db, chat_id)
>>>>>>> main
