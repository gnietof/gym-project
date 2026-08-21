import datetime
import uuid
from typing import ClassVar

from sqlalchemy import UUID, DateTime, Integer, Numeric, String, event, text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, declarative_base, mapped_column

from common.db.database import engine

Base = declarative_base()

SCHEMA = "log2"


class Usage(Base):
    """Models the information stored in the database to track LLM's usage"""

    __tablename__: ClassVar[str] = "usages"
    __table_args__: ClassVar[dict] = {"schema": SCHEMA}

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    provider: Mapped[str] = mapped_column(String(50), nullable=False)
    model: Mapped[str] = mapped_column(String(50), nullable=False)
    prompt: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=True)

    session: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True))
    track: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), unique=True, server_default=text("gen_random_uuid()")
    )

    score: Mapped[str] = mapped_column(String, nullable=True)

    messages_sent: Mapped[list[dict]] = mapped_column(JSONB, nullable=False)
    tools_provided: Mapped[list[dict] | None] = mapped_column(JSONB, nullable=True)
    response_received: Mapped[dict] = mapped_column(JSONB, nullable=False)

    tag: Mapped[str] = mapped_column(String[20], nullable=False)

    prompt_tokens: Mapped[int] = mapped_column(Integer, default=0)
    completion_tokens: Mapped[int] = mapped_column(Integer, default=0)
    total_tokens: Mapped[int] = mapped_column(Integer, default=0)

    cost: Mapped[float | None] = mapped_column(
        Numeric(precision=10, scale=6), nullable=True
    )

    timestamp: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.datetime.now(datetime.timezone.utc),
    )


@event.listens_for(Base.metadata, "before_create")
def receive_before_create(target, connection, **kw):
    connection.execute(text("CREATE SCHEMA IF NOT EXISTS log"))


Base.metadata.create_all(engine)
