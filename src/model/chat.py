from dataclasses import dataclass

from pydantic import BaseModel

class ChatRequest(BaseModel):
  id: str | None = None
  question: str

class ChatResponse(BaseModel):
  id: str | None = None
  answer: str
