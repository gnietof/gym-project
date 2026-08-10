from typing import ClassVar

from pgvector.sqlalchemy import Vector
from sqlalchemy import Column, SmallInteger, String, Text
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Activity(Base):
    """Represents the description of a gym activity"""

    __tablename__: ClassVar[str] = "activities"
    __table_args__: ClassVar[dict] = {"schema": "gym"}

    id = Column(SmallInteger, primary_key=True, autoincrement=True)
    activity_name = Column(String)
    category = Column(String)
    subcategory = Column(String)
    full_description = Column(Text)
    embedding = Column(Vector(1536))
