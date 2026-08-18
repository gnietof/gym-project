from sqlalchemy.orm import declarative_base

Base = declarative_base()


# class Session(Base):
#     """Represents the description of a gym activity"""

#     __tablename__: ClassVar[str] = "sessions"
#     __table_args__: ClassVar[dict] = {"schema": "gym"}

#     id: Mapped[int] = mapped_column(SmallInteger, primary_key=True, autoincrement=True)
#     activity_code: Mapped[str] = mapped_column(String)
#     activity_name = relationship(
#         "Activity",
#         primaryjoin="activity_code == Activity.activity_code",
#         foreign_keys="[Session.activity_code]",
#     )

#     time: Mapped[datetime.time] = mapped_column(Time(timezone=False))
#     day: Mapped[int] = mapped_column(SmallInteger)
#     duration: Mapped[int] = mapped_column(SmallInteger)
