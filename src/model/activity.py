from sqlalchemy import Column, Integer, SmallInteger, String, Text
from sqlalchemy.orm import declarative_base
from pgvector.sqlalchemy import Vector

Base = declarative_base()

class Activity(Base):
  """ Represents the description of a gym activity
  """
  __tablename__ = "activities" 
  __table_args__ = {"schema":"gym"}

  id = Column(SmallInteger, primary_key=True, autoincrement=True)
  activity_name = Column(String)
  category = Column(String)
  subcategory = Column(String)
  full_description = Column(Text)
  embedding = Column(Vector(1536))



