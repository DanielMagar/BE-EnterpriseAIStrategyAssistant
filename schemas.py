from pydantic import BaseModel
from typing import List, Dict

class Message(BaseModel):
    role: str
    text: str

class ChatRequest(BaseModel):
    provider: str
    conversation: List[Message]