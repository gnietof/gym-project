from typing import ClassVar

from sqlalchemy import Column, SmallInteger, String
from sqlalchemy.orm import Mapped, declarative_base, mapped_column

Base = declarative_base()


class Category(Base):
    """Represents the description of a gym activity category"""

    __tablename__: ClassVar[str] = "categories"
    __table_args__: ClassVar[dict] = {"schema": "gym"}

    id = Column(SmallInteger, primary_key=True, autoincrement=True)
    category = Column(String)


class Subcategory(Base):
    """Represents the description of a gym activity subcategory"""

    __tablename__: ClassVar[str] = "subcategories"
    __table_args__: ClassVar[dict] = {"schema": "gym"}

    id = Column(SmallInteger, primary_key=True, autoincrement=True)
    category = Column(SmallInteger)
    subcategory = Column(String)


class Intensity(Base):
    """Represents the description of the intensity of a gym activity"""

    __tablename__: ClassVar[str] = "intensity_levels"
    __table_args__: ClassVar[dict] = {"schema": "gym"}

    value: Mapped[int] = mapped_column(SmallInteger, primary_key=True)
    description: Mapped[str] = mapped_column(String)
