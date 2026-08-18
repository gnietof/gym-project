from typing import ClassVar

from sqlalchemy import SmallInteger, String
from sqlalchemy.orm import Mapped, declarative_base, mapped_column

Base = declarative_base()


class Question(Base):
    """Represents the description of a gym question"""

    __tablename__: ClassVar[str] = "questions"
    __table_args__: ClassVar[dict] = {"schema": "gym"}

    id: Mapped[int] = mapped_column(SmallInteger, primary_key=True, autoincrement=True)
    activity_name: Mapped[str] = mapped_column(String)
    question: Mapped[str] = mapped_column(String)
