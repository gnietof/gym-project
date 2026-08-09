import logging

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from chat.services import ask_question,score_answer
from common.db.dependencies import get_db
from dto.chat import ChatRequestDTO, ChatResponseDTO, ScoreRequestDTO

logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/ask", response_model=ChatResponseDTO)
async def ask(payload: ChatRequestDTO, db: Session = Depends(get_db)):
  id = payload.id
  question = payload.question

  logger.debug(f"Accepting question {question} for session {id}.")

  answer,track = await ask_question(question, db)
  response = ChatResponseDTO(id=id,answer=answer,track=track)
  return response

@router.post("/score")
async def score(payload: ScoreRequestDTO, db: Session = Depends(get_db)):
  id = payload.id
  track = payload.track
  mode = payload.mode
  
  logger.info(f"Scoring {mode} answer with track {track} .")

  await score_answer(track,mode, db)
