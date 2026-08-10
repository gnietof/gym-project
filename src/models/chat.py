from uuid import UUID

from pydantic import BaseModel


class ChatRequestDTO(BaseModel):
    id: str | None = None
    question: str


class ChatResponseDTO(BaseModel):
    id: str | None = None
    answer: str
    track: UUID


class ScoreRequestDTO(BaseModel):
    id: str | None = None
    mode: str
    track: str
