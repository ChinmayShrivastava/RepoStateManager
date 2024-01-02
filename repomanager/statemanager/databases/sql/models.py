from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
import uuid

from .database_init import Base

# class Element(Base):
#     __tablename__ = "elements"

#     id = Column(Integer, primary_key=True, index=True)
#     filename = Column(String, index=True)
#     content = Column(String, index=True)

#     # relationships
#     # related to a file in the files table
#     file = relationship("File", back_populates="elements")

# class File(Base):
#     __tablename__ = "files"

#     id = Column(Integer, primary_key=True, index=True)
#     filename = Column(String, index=True)
#     content = Column(String, index=True)

#     # relationships
#     # related to a file in the files table
#     elements = relationship("Element", back_populates="file")

class Chat(Base):
    __tablename__ = "chats"

    id = Column(Integer, primary_key=True, index=True)
    conversation = Column(String, index=True)
    tool_calls = Column(String, index=True)

    # relationships
    # related to a session in the session table
    session = relationship("Session", back_populates="chat")

class Session(Base):
    __tablename__ = "sessions"

    # session_id is uuid and unique
    session_id = Column(String, primary_key=True, index=True)

    # relationships
    # related to a chat in the chat table
    chat = relationship("Chat", back_populates="session")

    # automatically add a session_id at creation
    def __init__(self, session_id):
        self.session_id = uuid.uuid4().hex