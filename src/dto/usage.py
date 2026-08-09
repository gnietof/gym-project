import datetime

from sqlmodel import SQLModel

class UsageDTO(SQLModel):
  timestamp: datetime.datetime
  provider: str
  model: str
  prompt_tokens: int
  completion_tokens: int
  total_tokens: int

  class Config:
    from_attributes = True



