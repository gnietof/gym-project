"""Gemini Helper
Helper module to centralize the access to Gemini calls so that they are also tracked
"""

import logging

from google import genai
from google.genai import errors, types

_gemini_client: genai.Client | None = None

logger = logging.getLogger(__name__)


def get_gemini_client() -> genai.Client:
    global _gemini_client

    if _gemini_client is None:
        _gemini_client = genai.Client()

    return _gemini_client


def count(contents: str, model) -> int:
    client = get_gemini_client()
    count_response = client.models.count_tokens(model=model, contents=contents)
    if not count_response:
        logger.error("Counting tokens in embed failed")
        return 0
    tokens_used = count_response.total_tokens
    return tokens_used


def embed(contents: str, model) -> list[float]:
    client = get_gemini_client()

    try:
        response = client.models.embed_content(
            model=model,
            contents=contents,
            config=types.EmbedContentConfig(output_dimensionality=1536),
        )

    except errors.APIError as e:
        logger.info(f"Exception while calling LLM embed: {e}")

    return response
