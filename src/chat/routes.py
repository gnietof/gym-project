from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from chat.services import ask_question
from common.db.dependencies import get_db
from model.chat import ChatRequest, ChatResponse

router = APIRouter()

@router.post("/ask", response_model=ChatResponse)
async def ask(payload: ChatRequest, db: Session = Depends(get_db)):
  id = payload.id
  question = payload.question
  answer = await ask_question(question, db)
  response = ChatResponse(id=id,answer=answer)
  return response
