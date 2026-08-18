from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from common.db.dependencies import get_db
from models.session import SessionDTO
from services.session_services import (
    get_sessions_service,
)

router = APIRouter()


@router.get("/sessions", response_model=list[SessionDTO])
def get_sessions_endpoint(db: Session = Depends(get_db)):
    records = get_sessions_service(db)
    return [SessionDTO.model_validate(record) for record in records]
