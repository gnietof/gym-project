import datetime

from sqlmodel import SQLModel


class SessionDTO(SQLModel):
    """Represents the description of a gym activity session"""

    activity_name: str

    time: datetime.time
    duration: int
    day: int

    is_new: str
    weights_used: str
