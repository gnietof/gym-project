import datetime
from uuid import UUID

from sqlmodel import SQLModel


class PromptDTO(SQLModel):
    timestamp: datetime.datetime
    prompt: UUID
    template: str
    tag: str
    active: str

    class Config:
        from_attributes = True
