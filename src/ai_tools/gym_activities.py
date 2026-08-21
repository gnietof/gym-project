import logging

from ai_services.gemini import count, embed
from ai_services.groq import create
from repository.activity_repo import vector_search
from repository.propmpt_repo import get_prompt_by_tag
from repository.usage_repo import UsageTrack

logger = logging.getLogger(__name__)


def retrieve_gym_activities(db: any, id: str, model, question: str):

    logger.info(f"Calling retrieve_gym_activities to answer: {question}")

    usage_track = UsageTrack(db, id)

    # Question embedding. Counting tokens for usage tracking
    tokens = count(question, "gemini-embedding-001")
    response = embed(question, "gemini-embedding-001")
    if not response:
        logger.error("Question embedding failed.")
        return "Sorry, could not find matching context for that question."
    usage_track.track_embed(
        "gemini-embedding-001", "gym_activities_embed", question, tokens, response
    )

    # Document search using the generated embedding
    query_vector = response.embeddings[0].values
    descriptions = vector_search(db, query_vector)

    if not descriptions:
        logger.warning("Search did not return any documents.")
        return "Sorry, could not find matching context for that question."

    # Build context with retrieved documents
    context = [description.content for description in descriptions]
    full_context = "\n\n---\n\n".join(context)

    prompt = get_prompt_by_tag(db, "gym_activities_create")

    template = prompt.template.format(context=full_context)

    messages = [
        {"role": "system", "content": template},
        {"role": "user", "content": question},
    ]

    # Generate the response using the LLM
    response = create(messages, model, prompt.tag, [])
    usage_track.track_create(
        model,
        "gym_activities",
        prompt.prompt,
        messages,
        [],
        response,
    )

    message = response.choices[0].message.content

    return {"retrieved_info": message}
