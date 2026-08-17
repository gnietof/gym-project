import logging

from sqlalchemy import text

from ai_services.groq import create
from repository.propmpt_repo import get_prompt_by_tag
from repository.usage_repo import UsageTrack

logger = logging.getLogger(__name__)


def retrieve_gym_sessions(db: any, id: str, model: str, question: str):

    usage_track = UsageTrack(db, id)

    prompt = get_prompt_by_tag(db, "gym_sessions")

    messages = [
        {"role": "system", "content": prompt.template},
        {"role": "user", "content": question},
    ]

    logger.info(f"Calling retrieve_gym_activities to answer: {question}")

    query = create(messages, model, prompt.tag, [])
    response = create(messages, model, "gym_activities_create", [])
    usage_track.track_create(
        model,
        "gym_sessions",
        prompt.prompt,
        messages,
        [],
        response,
    )

    sql = text(query.choices[0].message.content.replace("```", ""))

    print(f"\n{sql}")

    result = db.execute(sql)
    schedule = [dict(row) for row in result.mappings()]

    return schedule
