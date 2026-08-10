"""Gemini Helper
Helper module to centralize the access to Gemini calls so that they are also tracked
"""

import logging

from google import genai
from google.genai import errors, types
from sqlalchemy.exc import SQLAlchemyError

from common.db.database import SessionLocal
from schemas.usage import Usage

_gemini_client: genai.Client | None = None

logger = logging.getLogger(__name__)


def get_gemini_client() -> genai.Client:
    global _gemini_client

    if _gemini_client is None:
        _gemini_client = genai.Client()

    return _gemini_client


def embed(contents: str, model="gemini-embedding-001") -> list[float]:
    client = get_gemini_client()

    try:
        count_response = client.models.count_tokens(model=model, contents=contents)
        tokens_used = count_response.total_tokens

        response = _gemini_client.models.embed_content(
            model=model,
            contents=contents,
            config=types.EmbedContentConfig(output_dimensionality=1536),
        )
        embedding_vector = response.embeddings[0].values

    except errors.APIError as e:
        logger.info(f"Exception while calling LLM embed: {e}")

    try:
        with SessionLocal() as session:
            usage = Usage(
                provider="GEMINI",
                model=model,
                messages_sent=contents,
                tools_provided=[],
                response_received=response.model_dump(),
                tag="embed_text",
                prompt_tokens=tokens_used,
                completion_tokens=0,
                total_tokens=tokens_used,
            )
            session.add(usage)
            session.commit()

    except SQLAlchemyError as e:
        logger.info(f"Exception while storing LLM call in database: {e}")

    return embedding_vector
