import logging
import uuid

from sqlalchemy import text

from ai_services.groq import create
from repository.propmpt_repo import get_prompt_by_tag
from repository.usage_repo import UsageTrack

logger = logging.getLogger(__name__)


def retrieve_gym_sessions(db: any, id: str, model: str, question: str):

    usage_track = UsageTrack(db, id)

    prompt = get_prompt_by_tag(db, "gym_sessions")

    # system_prompt = """
    #   You are an expert PostgreSQL generator. Your sole task is to turn user requests into a single executable SQL query for the GYM.VW_SESSIONS table.

    #   CRITICAL RULES:
    #   1. Always include the DOW (Day of Week) and TIME columns in the SELECT clause so the user knows exactly when the activity happens.
    #   2. Return ONLY the raw SQL query string.
    #   3. Do NOT wrap it in markdown code blocks (```sql).
    #   4. Do NOT use surrounding quotes, and do NOT include any conversational filler.

    #   TABLE SCHEMA:
    #   Table: GYM.VW_SESSIONS
    #   - ACTIVITY_NAME (VARCHAR): Name of the fitness activity/class.
    #   - TIME (TIME): Scheduled time in HH:MM 24-hour format (e.g., 18:30).
    #   - DOW (VARCHAR): Day of the week in lower case (e.g., monday, tuesday ...).
    #   - DURATION (INT): Duration of the activity in minutes.

    #   EXAMPLE OUPUT:
    #   SELECT ACTIVITY_NAME, DOW, TIME, DURATION FROM GYM.VW_SESSIONS WHERE LOWER(ACTIVITY_NAME) LIKE '%yoga%'
    # """

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
        # prompt.prompt,
        uuid.uuid4(),
        messages,
        [],
        response,
    )

    sql = text(query.choices[0].message.content.replace("```", ""))

    print(f"\n{sql}")

    # with SessionLocal() as db:
    result = db.execute(sql)
    schedule = [dict(row) for row in result.mappings()]

    return schedule
