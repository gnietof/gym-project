import logging

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from common.db.dependencies import get_db
from models.usage import DetailDTO, RequestDTO, ScoreDTO, UsageDTO
from services.usage_services import (
    get_request_by_track_service,
    get_requests_service,
    get_scores_service,
    get_usages_service,
)

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/tokens", response_model=list[UsageDTO])
def get_tokens_endpoint(db: Session = Depends(get_db)):
    logger.debug("Requested a list of tokens usage.")
    records = get_usages_service(db)
    return [UsageDTO.model_validate(record) for record in records]


@router.get("/scores", response_model=list[ScoreDTO])
def get_scores_endpoint(db: Session = Depends(get_db)):
    logger.debug("Requested a list of answer scores.")
    records = get_scores_service(db)
    return [ScoreDTO.model_validate(record) for record in records]


@router.get("/requests", response_model=list[RequestDTO])
def get_requests_endpoint(db: Session = Depends(get_db)):
    logger.debug("Requested a list of llm requests.")
    records = get_requests_service(db)
    return [RequestDTO.model_validate(record) for record in records]


@router.get("/requests/{track}", response_model=DetailDTO)
def get_request_by_track_endpoint(track: str, db: Session = Depends(get_db)):
    logger.debug(f"Request llm request with track id {track}.")
    record = get_request_by_track_service(track, db)
    return DetailDTO.model_validate(record)
