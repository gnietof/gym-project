from sqlalchemy import select

from schemas.activity import Activity


def vector_search(db: any, query_vector: list[float], limit=5) -> list[Activity]:

    query = (
        select(Activity)
        .order_by(Activity.embedding.cosine_distance(query_vector))
        .limit(limit)
    )

    result = db.execute(query)
    closest = result.scalars().all()

    return closest
