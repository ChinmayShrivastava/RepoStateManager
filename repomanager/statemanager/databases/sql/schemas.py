from typing import List, Union
from pydantic import BaseModel

class ChatBase(BaseModel):
    conversation: str
    tool_calls: str

class ChatCreate(ChatBase):
    pass

class Chat(ChatBase):
    id: int
    session_id: int

    class Config:
        from_attributes = True

class SessionBase(BaseModel):
    session_id: str

class SessionCreate(SessionBase):
    pass

class Session(SessionBase):
    id: int
    chat: List[Chat] = []

    class Config:
        from_attributes = True