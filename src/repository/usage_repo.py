import logging

from sqlalchemy import and_, func, select, update
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from schemas.usage import Usage

logger = logging.getLogger(__name__)


class UsageTrack:
    def __init__(self, db: Session, id: str):
        self.db = db
        self.id = id

    def track_create(
        self,
        model: str,
        # prompt: Prompt,
        tag: str,
        prompt: str,
        messages: list[dict],
        tools: list[dict],
        response: dict,
    ):
        try:
            usage = Usage(
                session=self.id,
                provider="GROQ",
                model=model,
                messages_sent=messages,
                tools_provided=tools,
                response_received=response.model_dump(),
                # tag=prompt.tag,
                tag=tag,
                prompt_tokens=response.usage.prompt_tokens,
                completion_tokens=response.usage.completion_tokens,
                total_tokens=response.usage.total_tokens,
                # prompt=prompt.prompt,
                prompt=prompt,
            )
            self.db.add(usage)
            self.db.commit()
            self.db.refresh(usage)

            return usage.track

        except SQLAlchemyError as e:
            logger.info(f"Exception while storing LLM call in database: {e}")

    def track_embed(
        self,
        model: str,
        tag: str,
        contents: str,
        tokens_used: int,
        response: dict,
    ):
        try:
            usage = Usage(
                session=self.id,
                provider="GEMINI",
                model=model,
                messages_sent=contents,
                response_received=response.model_dump(),
                tag=tag,
                prompt_tokens=tokens_used,
                completion_tokens=0,
                total_tokens=tokens_used,
            )
            self.db.add(usage)
            self.db.commit()
            return usage.track

        except SQLAlchemyError as e:
            logger.info(f"Exception while storing LLM call in database: {e}")


class UsageRepo:
    def __init__(self, db: Session):
        self.db = db

    def get_all_usages(self) -> list[Usage]:
        query = select(
            Usage.timestamp,
            Usage.provider,
            Usage.model,
            Usage.prompt_tokens,
            Usage.completion_tokens,
            Usage.total_tokens,
        ).order_by(Usage.timestamp.desc())

        records = self.db.execute(query)

        return records

    def get_all_scores(self) -> list[any]:
        query = (
            select(
                Usage.timestamp,
                Usage.model,
                func.count().filter(Usage.score == "U").label("up"),
                func.count().filter(Usage.score == "D").label("down"),
            )
            .where(Usage.provider == "GROQ")
            .group_by(Usage.model, Usage.timestamp)
        )

        records = self.db.execute(query)

        return records

    def get_all_requests(self) -> list[any]:
        query = (
            select(
                Usage.timestamp,
                Usage.model,
                Usage.track,
                Usage.session,
                Usage.prompt_tokens,
                Usage.completion_tokens,
                Usage.total_tokens,
                Usage.tag,
                func.coalesce(Usage.score, "").label("score"),
            )
            .filter(Usage.provider == "GROQ")
            .order_by(Usage.timestamp.desc())
        )

        records = self.db.execute(query)

        return records

    def get_request_by_track(self, track: str) -> list[any]:
        query = select(
            Usage.timestamp,
            Usage.model,
            Usage.track,
            Usage.session,
            Usage.prompt_tokens,
            Usage.completion_tokens,
            Usage.total_tokens,
            Usage.messages_sent,
            Usage.response_received,
            Usage.tag,
            func.coalesce(Usage.score, "").label("score"),
        ).where(and_(Usage.provider == "GROQ", Usage.track == track))

        record = self.db.execute(query).first()

        return record


class UsageScore:
    def __init__(self, db: Session):
        self.db = db

    def update_score(self, track: str, mode: str):
        new_score = "U" if mode == "up" else ("D" if mode == "down" else "")

        stmt = update(Usage).where(Usage.track == track).values(score=new_score)
        result = self.db.execute(stmt)
        self.db.commit()

        if result.rowcount > 0:
            logger.info(f"Track {track} score added.")
        else:
            logger.info(f"Track {track} not found for scoring!")


# def track_create(
#     id: str,
#     model: str,
#     prompt: Prompt,
#     messages: list[dict],
#     tools: list[dict],
#     response: dict,
#     db: any,
# ):
#     try:
#         usage = Usage(
#             session=id,
#             provider="GROQ",
#             model=model,
#             messages_sent=messages,
#             tools_provided=tools,
#             response_received=response.model_dump(),
#             tag=prompt.tag,
#             prompt_tokens=response.usage.prompt_tokens,
#             completion_tokens=response.usage.completion_tokens,
#             total_tokens=response.usage.total_tokens,
#             prompt=prompt.prompt,
#         )
#         db.add(usage)
#         db.commit()
#         db.refresh(usage)

#         return usage

#     except SQLAlchemyError as e:
#         logger.info(f"Exception while storing LLM call in database: {e}")


# def track_embed(
#     id: str,
#     model: str,
#     tag: str,
#     contents: str,
#     tokens_used: int,
#     response: dict,
#     db: any,
# ):
#     try:
#         usage = Usage(
#             session=id,
#             provider="GEMINI",
#             model=model,
#             messages_sent=contents,
#             tools_provided=[],
#             response_received=response.model_dump(),
#             tag=tag,
#             prompt_tokens=tokens_used,
#             completion_tokens=0,
#             total_tokens=tokens_used,
#         )
#         db.add(usage)
#         db.commit()

#     except SQLAlchemyError as e:
#         logger.info(f"Exception while storing LLM call in database: {e}")


# def get_all_usages(db: any) -> list[Usage]:
#     query = select(
#         Usage.timestamp,
#         Usage.provider,
#         Usage.model,
#         Usage.prompt_tokens,
#         Usage.completion_tokens,
#         Usage.total_tokens,
#     ).order_by(Usage.timestamp.desc())

#     records = db.execute(query)

#     return records


# def get_all_scores(db: any) -> list[any]:
#     query = (
#         select(
#             Usage.model,
#             func.count().filter(Usage.score == "U").label("up"),
#             func.count().filter(Usage.score == "D").label("down"),
#         )
#         .where(Usage.provider == "GROQ")
#         .group_by(Usage.model)
#     )

#     records = db.execute(query)

#     return records


# def get_all_requests(db: any) -> list[any]:
#     query = (
#         select(
#             Usage.timestamp,
#             Usage.model,
#             Usage.track,
#             Usage.session,
#             Usage.prompt_tokens,
#             Usage.completion_tokens,
#             Usage.total_tokens,
#             Usage.tag,
#             func.coalesce(Usage.score, "").label("score"),
#         )
#         .filter(Usage.provider == "GROQ")
#         .order_by(Usage.timestamp.desc())
#     )

#     records = db.execute(query)

#     return records


# def get_request_by_track(db: any, track: str) -> list[any]:
#     query = select(
#         Usage.timestamp,
#         Usage.model,
#         Usage.track,
#         Usage.session,
#         Usage.prompt_tokens,
#         Usage.completion_tokens,
#         Usage.total_tokens,
#         Usage.messages_sent,
#         Usage.response_received,
#         Usage.tag,
#         func.coalesce(Usage.score, "").label("score"),
#     ).where(and_(Usage.provider == "GROQ", Usage.track == track))

#     record = db.execute(query).first()

#     return record
