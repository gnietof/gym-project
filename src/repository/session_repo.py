from sqlalchemy import case, select

from schemas.activity import Activity, Session


def get_all_sessions(db: any) -> list[Session]:
    query = select(
        Session.time,
        Session.duration,
        Session.day,
        Activity.activity_name,
        case((Activity.is_new == True, "Yes"), else_="No").label("is_new"),
        case((Activity.weights_used == True, "Yes"), else_="No").label("weights_used"),
    ).join(Activity, Session.activity_map)
    sessions = db.execute(query).all()

    return sessions
