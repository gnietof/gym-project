from typing import ClassVar

from pgvector.sqlalchemy import Vector
from sqlalchemy import Boolean, Column, SmallInteger, String, Text, and_
from sqlalchemy.orm import declarative_base, relationship

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


class GymLevels:
    __table_args__: ClassVar[dict] = {"schema": "gym"}

    value = Column(SmallInteger, primary_key=True)
    description = Column(String)


class Intensity(GymLevels, Base):
    """Represents the description of the intensity of a gym activity"""

    __tablename__: ClassVar[str] = "intensity_levels"


class Skill(GymLevels, Base):
    """Represents the description of the intensity of a gym activity"""

    __tablename__: ClassVar[str] = "skill_levels"


class Impact(GymLevels, Base):
    """Represents the description of the intensity of a gym activity"""

    __tablename__: ClassVar[str] = "impact_levels"


class CaloricBurn(GymLevels, Base):
    """Represents the description of the intensity of a gym activity"""

    __tablename__: ClassVar[str] = "caloric_burns"


class Activity(Base):
    """Represents the description of a gym activity"""

    __tablename__: ClassVar[str] = "activities"
    __table_args__: ClassVar[dict] = {"schema": "gym"}

    id = Column(SmallInteger, primary_key=True, autoincrement=True)
    activity_code = Column(String)
    activity_name = Column(String)

    category = Column(SmallInteger)
    category_name = relationship(
        "Category",
        primaryjoin=category == Category.id,
        foreign_keys=[category],
    )

    subcategory = Column(SmallInteger)
    subcategory_name = relationship(
        "Subcategory",
        primaryjoin=and_(
            category == Subcategory.category, subcategory == Subcategory.id
        ),
        foreign_keys="[Activity.subcategory]",
    )

    intensity_level = Column(SmallInteger)
    intensity_level_name = relationship(
        "Intensity",
        primaryjoin=intensity_level == Intensity.value,
        foreign_keys="[Activity.intensity_level]",
    )

    weights_used = Column(Boolean)

    skill_level = Column(SmallInteger)
    skill_level_name = relationship(
        "Skill",
        primaryjoin=skill_level == Skill.value,
        foreign_keys="[Activity.skill_level]",
    )

    impact_level = Column(SmallInteger)
    impact_level_name = relationship(
        "Impact",
        primaryjoin=impact_level == Impact.value,
        foreign_keys="[Activity.impact_level]",
    )

    caloric_burn = Column(SmallInteger)
    caloric_burn_name = relationship(
        "CaloricBurn",
        primaryjoin=caloric_burn == CaloricBurn.value,
        foreign_keys="[Activity.caloric_burn]",
    )

    full_description = Column(Text)
    embedding = Column(Vector(1536))


Base = declarative_base()
