from fastapi import logger
from sqlalchemy import select

from model.activity import Activity
from services.gemini import embed
from services.groq import create

LLAMA31_8B = "llama-3.1-8b-instant"

async def ask_question(question: str, db: any, model=LLAMA31_8B) -> str:
  activities = _semantic_search(db,question)

  if not activities:
    return "Sorry, could not find matching context for that question."

  context = []
  for activity in activities:
    context.append(activity.full_description)

  full_context = "\n\n---\n\n".join(context)

  system_prompt = (
    "You are an expert Gym and Fitness AI assistant. Your job is to answer user questions "
    "accurately using ONLY the verified context provided below. If the answer cannot be "
    "found in the context, politely state that you do not know."
    "Do NOT add anything which is not in the infomration provided\n\n"
    f"--- START CONTEXT ---\n{full_context}\n--- END CONTEXT ---"
    )  

  messages = [
    {"role":"system","content":system_prompt},
    {"role":"user","content":question},
  ]

  try: 
    answer = create(messages,model,"gym_assistant",[])
    # logger.debug(f"\nQUESTION: {question}\nANSWER: {answer}\n")
    return answer

  except Exception as e:
    # logger.error(f"An exception occurred when generating the LLM answer: {e}")
    print(f"An exception occurred when generating the LLM answer: {e}")

def _semantic_search(db: any, question:str, limit: int=5) -> list[Activity]:
    
  query_vector = embed(question)

  query = (select(Activity)
          .order_by(Activity.embedding.cosine_distance(query_vector))
          .limit(limit))

  result= db.execute(query)
  closest = result.scalars().all()

  return closest