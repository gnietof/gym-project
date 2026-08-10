import logging

from sqlalchemy import select

from ai_services.gemini import embed
from ai_services.groq import create
from repository.propmpt_repo import get_prompt_by_tag
from repository.usage_repo import track_request
from schemas.activity import Activity
from schemas.usage import Usage

LLAMA31_8B = "llama-3.1-8b-instant"

logger = logging.getLogger(__name__)


async def score_answer(track: str, mode: str, db: any):
    usage = db.query(Usage).where(Usage.track == track).first()
    if usage:
        usage.score = "U" if mode == "up" else ("D" if mode == "down" else "")
        db.commit()
        logger.info(f"Track {track} score added.")
    else:
        logger.info(f"Track {track} not found for scoring!")


async def ask_question(question: str, tag: str, db: any, model=LLAMA31_8B) -> str:
    activities = _semantic_search(db, question)

    if not activities:
        return "Sorry, could not find matching context for that question."

    context = []
    for activity in activities:
        context.append(activity.full_description)

    full_context = "\n\n---\n\n".join(context)

    # system_prompt = (
    #   "You are an expert Gym and Fitness AI assistant. Your job is to answer user questions "
    #   "accurately using ONLY the verified context provided below. If the answer cannot be "
    #   "found in the context, politely state that you do not know."
    #   "Do NOT add anything which is not in the infomration provided\n\n"
    #   f"--- START CONTEXT ---\n{full_context}\n--- END CONTEXT ---"
    #   )

    prompt = get_prompt_by_tag(db, tag)
    if not prompt:
        return ""

    template = prompt.template.format(context=full_context)

    messages = [
        {"role": "system", "content": template},
        {"role": "user", "content": question},
    ]

    response = create(messages, model, tag, [])
    usage = track_request(model, prompt, messages, [], response, db)

    answer = response.choices[0].message.content
    track = usage.track

    return answer, track


def _semantic_search(db: any, question: str, limit: int = 5) -> list[Activity]:

    query_vector = embed(question)

    query = (
        select(Activity)
        .order_by(Activity.embedding.cosine_distance(query_vector))
        .limit(limit)
    )

    result = db.execute(query)
    closest = result.scalars().all()

    return closest
