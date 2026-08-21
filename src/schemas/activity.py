import datetime
from typing import ClassVar

from pgvector.sqlalchemy import Vector
from sqlalchemy import Boolean, SmallInteger, String, Text, Time, and_
from sqlalchemy.orm import Mapped, declarative_base, mapped_column, relationship

Base = declarative_base()

SCHEMA = "gym2"


class Category(Base):
    """Represents the description of a gym activity category"""

    __tablename__: ClassVar[str] = "categories"
    __table_args__: ClassVar[dict] = {"schema": SCHEMA}

    id: Mapped[int] = mapped_column(SmallInteger, primary_key=True, autoincrement=True)
    category: Mapped[str] = mapped_column(String)


class Subcategory(Base):
    """Represents the description of a gym activity subcategory"""

    __tablename__: ClassVar[str] = "subcategories"
    __table_args__: ClassVar[dict] = {"schema": SCHEMA}

    id: Mapped[int] = mapped_column(SmallInteger, primary_key=True, autoincrement=True)
    category: Mapped[int] = mapped_column(SmallInteger)
    subcategory: Mapped[str] = mapped_column(String)


class GymLevels:
    __table_args__: ClassVar[dict] = {"schema": SCHEMA}

    value: Mapped[int] = mapped_column(SmallInteger, primary_key=True)
    description: Mapped[str] = mapped_column(String)


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
    __table_args__: ClassVar[dict] = {"schema": SCHEMA}

    # id: Mapped[int] = mapped_column(SmallInteger, primary_key=True, autoincrement=True)
    # id: Mapped[int] = mapped_column(SmallInteger)
    activity_code: Mapped[str] = mapped_column(String, primary_key=True)
    activity_name: Mapped[str] = mapped_column(String)

    category: Mapped[int] = mapped_column(SmallInteger)
    category_name = relationship(
        "Category",
        primaryjoin=category == Category.id,
        foreign_keys=[category],
    )

    subcategory: Mapped[int] = mapped_column(SmallInteger)
    subcategory_name = relationship(
        "Subcategory",
        primaryjoin=and_(
            category == Subcategory.category, subcategory == Subcategory.id
        ),
        foreign_keys="[Activity.subcategory]",
    )

    intensity_level: Mapped[int] = mapped_column(SmallInteger)
    intensity_map: Mapped[Intensity] = relationship(
        "Intensity",
        primaryjoin=intensity_level == Intensity.value,
        foreign_keys="[Activity.intensity_level]",
    )

    weights_used: Mapped[bool] = mapped_column(Boolean)

    skill_level: Mapped[int] = mapped_column(SmallInteger)
    skill_map: Mapped[Skill] = relationship(
        "Skill",
        primaryjoin=skill_level == Skill.value,
        foreign_keys="[Activity.skill_level]",
    )

    impact_level: Mapped[int] = mapped_column(SmallInteger)
    impact_map: Mapped[Impact] = relationship(
        "Impact",
        primaryjoin=impact_level == Impact.value,
        foreign_keys="[Activity.impact_level]",
    )

    caloric_burn: Mapped[int] = mapped_column(SmallInteger)
    caloric_burn_map: Mapped[CaloricBurn] = relationship(
        "CaloricBurn",
        primaryjoin=caloric_burn == CaloricBurn.value,
        foreign_keys="[Activity.caloric_burn]",
    )

    is_new: Mapped[bool] = mapped_column(Boolean)

    description: Mapped[str] = mapped_column(Text)
    primary_benefit: Mapped[str] = mapped_column(Text)
    contraindications: Mapped[str] = mapped_column(Text)
    interesting_fact: Mapped[str] = mapped_column(Text)

    # full_description = Column(Text)
    # embedding = Column(Vector(1536))


class Embedding(Base):
    """Represents the embedding of a gym activity"""

    __tablename__: ClassVar[str] = "embeddings"
    __table_args__: ClassVar[dict] = {"schema": "gym2"}

    # id: Mapped[int] = mapped_column(SmallInteger, primary_key=True, autoincrement=True)
    activity_code: Mapped[str] = mapped_column(String, primary_key=True)
    activity_name: Mapped[str] = mapped_column(String)

    content: Mapped[str] = mapped_column(Text)
    embedding: Mapped[list[float]] = mapped_column(Vector(1536))


class Session(Base):
    """Represents the description of a gym activity"""

    __tablename__: ClassVar[str] = "sessions"
    __table_args__: ClassVar[dict] = {"schema": SCHEMA}

    id: Mapped[int] = mapped_column(SmallInteger, primary_key=True, autoincrement=True)
    activity_code: Mapped[str] = mapped_column(String)
    activity_map: Mapped[Activity] = relationship(
        "Activity",
        primaryjoin=activity_code == Activity.activity_code,
        foreign_keys="[Session.activity_code]",
    )

    time: Mapped[datetime.time] = mapped_column(Time(timezone=False))
    day: Mapped[int] = mapped_column(SmallInteger)
    duration: Mapped[int] = mapped_column(SmallInteger)
