from typing import ClassVar

from sqlalchemy import Column, SmallInteger, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Session(Base):
    """Represents the description of a gym activity"""

    __tablename__: ClassVar[str] = "sessions"
    __table_args__: ClassVar[dict] = {"schema": "gym"}

    id = Column(SmallInteger, primary_key=True, autoincrement=True)
    activity_code = Column(String)
    time = Column(String)
    day = Column(SmallInteger)
    duration = Column(SmallInteger)
