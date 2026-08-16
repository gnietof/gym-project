from typing import ClassVar

from sqlalchemy import Column, SmallInteger, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Question(Base):
    """Represents the description of a gym question"""

    __tablename__: ClassVar[str] = "questions"
    __table_args__: ClassVar[dict] = {"schema": "gym"}

    id = Column(SmallInteger, primary_key=True, autoincrement=True)
    activity_name = Column(String)
    question = Column(String)
