from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from common.db.dependencies import get_db
from dto.usage import UsageDTO
from usage.services import get_usage

router = APIRouter()

@router.get("/tokens", response_model=list[UsageDTO])
def usage(db: Session = Depends(get_db)):
  records = get_usage(db)
  return [UsageDTO.model_validate(record) for record in records]
  


