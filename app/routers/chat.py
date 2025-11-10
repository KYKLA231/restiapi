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
