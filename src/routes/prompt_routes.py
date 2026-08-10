import logging

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from common.db.dependencies import get_db
from models.prompt import PromptDTO
from services.prompt_services import get_prompts_service

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/prompts", response_model=list[PromptDTO])
def get_prompts_endpoint(db: Session = Depends(get_db)):
    logger.debug("Requested a list of defined prompts.")
    records = get_prompts_service(db)
    return [PromptDTO.model_validate(record) for record in records]
