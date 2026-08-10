import datetime
from uuid import UUID

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


class ScoreDTO(SQLModel):
    model: str
    up: int
    down: int

    class Config:
        from_attributes = True


class RequestDTO(SQLModel):
    timestamp: datetime.datetime
    model: str
    track: UUID
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int
    score: str
    tag: str

    class Config:
        from_attributes = True
