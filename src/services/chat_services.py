import logging

from ai_services.gemini import count, embed
from ai_services.groq import create
from repository.activity_repo import vector_search
from repository.propmpt_repo import get_prompt_by_tag
from repository.usage_repo import track_create, track_embed
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


async def ask_question(
    id: str, question: str, tag: str, db: any, model=LLAMA31_8B
) -> str:

    # Question embedding. Counting tokens for usage tracking
    tokens = count(question, "gemini-embedding-001")
    response = embed(question, "gemini-embedding-001")
    track_embed(
        id, "gemini-embedding-001", "embed_text", question, tokens, response, db
    )
    if not response:
        logger.error("Question embedding failed.")
        return "Sorry, could not find matching context for that question."

    # Document search using the generated embedding
    query_vector = response.embeddings[0].values
    activities = vector_search(db, query_vector)
    if not activities:
        logger.warning("Search did not return any documents.")
        return "Sorry, could not find matching context for that question."

    # Build context with retrieved documents
    context = []
    for activity in activities:
        context.append(activity.full_description)
    full_context = "\n\n---\n\n".join(context)

    prompt = get_prompt_by_tag(db, tag)
    if not prompt:
        return ""

    template = prompt.template.format(context=full_context)

    messages = [
        {"role": "system", "content": template},
        {"role": "user", "content": question},
    ]

    # Generate the response using the LLM
    response = create(messages, model, tag, [])
    usage = track_create(id, model, prompt, messages, [], response, db)

    answer = response.choices[0].message.content
    track = usage.track

    return answer, track
