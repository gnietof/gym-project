import logging

from sqlalchemy import and_, case, select

from schemas.prompt import Prompt

logger = logging.getLogger(__name__)


def get_all_prompts(db: any) -> list[Prompt]:
    query = select(
        Prompt.timestamp,
        Prompt.tag,
        case((Prompt.active == True, "Yes"), else_="No").label("active"),
        Prompt.prompt,
        Prompt.template,
    ).order_by(Prompt.timestamp.desc())

    records = db.execute(query)

    return records


def get_prompt_by_tag(db: any, tag: str) -> Prompt:

    query = select(
        Prompt.timestamp,
        Prompt.tag,
        case((Prompt.active == True, "Yes"), else_="No").label("active"),
        Prompt.prompt,
        Prompt.template,
    ).where(and_(Prompt.active, Prompt.tag == tag))

    record = db.execute(query).first()

    return record
