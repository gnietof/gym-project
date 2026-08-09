import datetime
from typing import List, Optional

from sqlalchemy import Column, DateTime, Integer, Numeric, String
from sqlalchemy.orm import Mapped, declarative_base, mapped_column
from sqlalchemy.dialects.postgresql import JSONB

from common.db.database import engine

Base = declarative_base()

class Usage(Base): 
  """ Models the information stored in the database to track LLM's usage
  """
  
  __tablename__ = "usages"
  __table_args__ = {"schema":"llm"}

  id: Mapped[int] = mapped_column(Integer,primary_key=True)
  provider: Mapped[str] = mapped_column(String(50),nullable=False)
  model: Mapped[str] = mapped_column(String(50),nullable=False)

  messages_sent: Mapped[List[dict]] = mapped_column(JSONB,nullable=False)
  tools_provided: Mapped[Optional[List[dict]]] = mapped_column(JSONB,nullable=False)
  response_received: Mapped[dict] = mapped_column(JSONB,nullable=False)

  tag: Mapped[str] = mapped_column(String[20],nullable=False)

  prompt_tokens: Mapped[int] = mapped_column(Integer, default=0)
  completion_tokens: Mapped[int] = mapped_column(Integer, default=0)
  total_tokens: Mapped[int] = mapped_column(Integer, default=0)  

  cost: Mapped[Optional[float]] = mapped_column(Numeric(precision=10, scale=6), nullable=True)
    
  timestamp: Mapped[datetime.datetime] = mapped_column(
    DateTime(timezone=True), 
    default=lambda: datetime.datetime.now(datetime.timezone.utc))  

Base.metadata.create_all(engine)
