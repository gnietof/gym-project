from sqlalchemy import Column, Integer, SmallInteger, String, Text
from sqlalchemy.orm import declarative_base
from pgvector.sqlalchemy import Vector

Base = declarative_base()

class Category(Base):
  """ Represents the description of a gym activity category
  """
  __tablename__ = "categories" 
  __table_args__ = {"schema":"gym"}

  id = Column(SmallInteger, primary_key=True, autoincrement=True)
  category = Column(String)

class Subcategory(Base):
  """ Represents the description of a gym activity subcategory
  """
  __tablename__ = "subcategories" 
  __table_args__ = {"schema":"gym"}

  id = Column(SmallInteger, primary_key=True, autoincrement=True)
  category = Column(SmallInteger)
  subcategory = Column(String)

class Intensity(Base):
  """ Represents the description of the intensity of a gym activity
  """
  __tablename__ = "intensity_levels" 
  __table_args__ = {"schema":"gym"}

  value = Column(SmallInteger, primary_key=True)
  description = Column(String)
