from sqlalchemy.orm import Session

from repository.session_repo import get_all_sessions


def get_sessions_service(db: any) -> list[Session]:
    sessions = get_all_sessions(db)
    return sessions
