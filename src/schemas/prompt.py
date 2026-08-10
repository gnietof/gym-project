import datetime
import uuid
from typing import ClassVar

from sqlalchemy import UUID, Boolean, DateTime, Integer, String, text
from sqlalchemy.orm import Mapped, declarative_base, mapped_column

from common.db.database import engine

Base = declarative_base()


class Prompt(Base):
    """Models a prompt which will be used for sending questions to the LLM"""

    __tablename__: ClassVar[str] = "prompts"
    __table_args__: ClassVar[dict] = {"schema": "llm"}

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    prompt: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), unique=True, server_default=text("gen_random_uuid()")
    )

    template: Mapped[str] = mapped_column(String)

    tag: Mapped[str] = mapped_column(String[20], nullable=False)
    active: Mapped[bool] = mapped_column(Boolean)

    timestamp: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.datetime.now(datetime.timezone.utc),
    )


Base.metadata.create_all(engine)
