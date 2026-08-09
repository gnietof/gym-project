import logging

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from common.db.dependencies import get_db
from dto.usage import RequestDTO, ScoreDTO, UsageDTO
from usage.services import get_requests, get_scores, get_usage

logger = logging.getLogger(__name__)

router = APIRouter()

@router.get("/tokens", response_model=list[UsageDTO])
def usage(db: Session = Depends(get_db)):
  records = get_usage(db)
  return [UsageDTO.model_validate(record) for record in records]
  
@router.get("/scores", response_model=list[ScoreDTO])
def usage(db: Session = Depends(get_db)):
  records = get_scores(db)
  return [ScoreDTO.model_validate(record) for record in records]
  
@router.get("/requests", response_model=list[RequestDTO])
def usage(db: Session = Depends(get_db)):
  records = get_requests(db)
  return [RequestDTO.model_validate(record) for record in records]
  


