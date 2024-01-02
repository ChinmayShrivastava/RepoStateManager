from sqlalchemy.orm import Session
from . import models, schemas

# CRUD for sessions

def get_session(db: Session, session_id: str):
    return db.query(models.Session).filter(models.Session.session_id == session_id).first()

def create_session(db: Session):
    db_session = models.Session()
    print(db_session.session_id)
    db.add(db_session)
    db.commit()
    db.refresh(db_session)
    return db_session

def create_chat(db: Session, chat: schemas.ChatCreate, session_id: str):
    db_chat = models.Chat(**chat.dict(), session_id=session_id)
    db.add(db_chat)
    db.commit()
    db.refresh(db_chat)
    return db_chat

def get_chat(db: Session, chat_id: int):
    return db.query(models.Chat).filter(models.Chat.id == chat_id).first()

def get_chats(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Chat).offset(skip).limit(limit).all()

def update_chat(db: Session, chat: schemas.Chat, chat_id: int):
    db_chat = db.query(models.Chat).filter(models.Chat.id == chat_id).first()
    db_chat.conversation = chat.conversation
    db_chat.tool_calls = chat.tool_calls
    db.commit()
    db.refresh(db_chat)
    return db_chat