import logging

from sqlalchemy import func, select
from sqlalchemy.exc import SQLAlchemyError

from schemas.prompt import Prompt
from schemas.usage import Usage

logger = logging.getLogger(__name__)


def track_request(
    model: str,
    prompt: Prompt,
    messages: list[dict],
    tools: list[dict],
    response: dict,
    db: any,
):
    try:
        usage = Usage(
            provider="GROQ",
            model=model,
            messages_sent=messages,
            tools_provided=tools,
            response_received=response.model_dump(),
            tag=prompt.tag,
            prompt_tokens=response.usage.prompt_tokens,
            completion_tokens=response.usage.completion_tokens,
            total_tokens=response.usage.total_tokens,
            prompt=prompt.prompt,
        )
        db.add(usage)
        db.commit()
        db.refresh(usage)

        return usage

    except SQLAlchemyError as e:
        logger.info(f"Exception while storing LLM call in database: {e}")


def get_all_usages(db: any) -> list[Usage]:
    query = select(
        Usage.timestamp,
        Usage.provider,
        Usage.model,
        Usage.prompt_tokens,
        Usage.completion_tokens,
        Usage.total_tokens,
    ).order_by(Usage.timestamp.desc())

    records = db.execute(query)

    return records


def get_all_scores(db: any) -> list[any]:
    query = (
        select(
            Usage.model,
            func.count().filter(Usage.score == "U").label("up"),
            func.count().filter(Usage.score == "D").label("down"),
        )
        .where(Usage.provider == "GROQ")
        .group_by(Usage.model)
    )

    records = db.execute(query)

    return records


def get_all_requests(db: any) -> list[any]:
    query = (
        select(
            Usage.timestamp,
            Usage.model,
            Usage.track,
            Usage.prompt_tokens,
            Usage.completion_tokens,
            Usage.total_tokens,
            Usage.tag,
            func.coalesce(Usage.score, "").label("score"),
        )
        .filter(Usage.provider == "GROQ")
        .order_by(Usage.timestamp.desc())
    )

    records = db.execute(query)

    return records
