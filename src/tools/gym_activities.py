import logging

from ai_services.gemini import embed
from ai_services.groq import create
from common.db.database import SessionLocal
from repository.activity_repo import vector_search

logger = logging.getLogger(__name__)


def retrieve_gym_activities(question: str, model="llama-3.1-8b-instant"):

    logger.info(f"Calling retrieve_gym_activities to answer: {question}")

    # Question embedding. Counting tokens for usage tracking
    response = embed(question, "gemini-embedding-001")
    if not response:
        logger.error("Question embedding failed.")
        return "Sorry, could not find matching context for that question."

    # Document search using the generated embedding
    query_vector = response.embeddings[0].values
    with SessionLocal() as db:
        descriptions = vector_search(db, query_vector)

    if not descriptions:
        logger.warning("Search did not return any documents.")
        return "Sorry, could not find matching context for that question."

    # Build context with retrieved documents
    context = []
    for description in descriptions:
        context.append(description.full_description)
    full_context = "\n\n---\n\n".join(context)

    prompt = (
        "You are an expert Gym and Fitness AI assistant. Your job is to answer user questions "
        "accurately using ONLY the verified context provided below. If the answer cannot be "
        "found in the context, politely state that you do not know."
        "Do NOT add anything which is not in the infomration provided\n\n"
        f"--- START CONTEXT ---\n{full_context}\n--- END CONTEXT ---"
    )

    template = prompt.format(context=full_context)

    messages = [
        {"role": "system", "content": template},
        {"role": "user", "content": question},
    ]

    # Generate the response using the LLM
    response = create(messages, model, "gym_activities", [])
    message = response.choices[0].message.content

    return {"retrieved_info": message}
