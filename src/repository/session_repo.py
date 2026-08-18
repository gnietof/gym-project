from sqlalchemy import select

from schemas.activity import (
    Activity,
    Session,
)


def get_all_sessions(db: any) -> list[Session]:
    query = select(
        Session.time,
        Session.duration,
        Session.day,
        Activity.activity_name,
        Activity.is_new,
    ).join(Activity, Session.activity_map)
    sessions = db.execute(query).all()

    return sessions


def vector_search(db: any, query_vector: list[float], limit=5) -> list[Activity]:

    query = (
        select(Activity)
        .order_by(Activity.embedding.cosine_distance(query_vector))
        .limit(limit)
    )

    closest = db.scalars(query).all()

    return closest
