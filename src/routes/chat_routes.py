import logging
import uuid

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from common.db.dependencies import get_db
from models.chat import ChatRequestDTO, ChatResponseDTO, ScoreRequestDTO
from services.chat_services import ask_question, score_answer

logger = logging.getLogger(__name__)

router = APIRouter()

sessions = {}

@router.post("/ask", response_model=ChatResponseDTO)
async def ask(payload: ChatRequestDTO, db: Session = Depends(get_db)):
    id = payload.id
    if not id:
        id = str(uuid.uuid4())
    if ()

    question = payload.question

    logger.debug(f"Accepting question {question} for session {id}.")

    answer, track = await ask_question(id, question, "gym_assistant", db)
    response = ChatResponseDTO(id=id, answer=answer, track=track)
    return response


@router.post("/score")
async def score(payload: ScoreRequestDTO, db: Session = Depends(get_db)):
    track = payload.track
    mode = payload.mode

    logger.info(f"Scoring {mode} answer with track {track} .")

    await score_answer(track, mode, db)
