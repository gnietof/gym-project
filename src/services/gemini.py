""" Gemini Helper
Helper module to centralize the access to Gemini calls so that they are also tracked
"""

from fastapi import logger
from google import genai
from google.genai import types

from common.ai.clients import get_gemini_client
from common.db.database import SessionLocal
from model.usage import Usage


gemini_client = get_gemini_client()

def embed(contents:str, model = "gemini-embedding-001") -> list[float]:

  try:

    count_response = gemini_client.models.count_tokens(
        model=model,
        contents=contents
    )
    tokens_used = count_response.total_tokens  

    response = gemini_client.models.embed_content(
      model= model,
      contents=contents,
      config=types.EmbedContentConfig(output_dimensionality=1536)
    )
    embedding_vector=response.embeddings[0].values

  except Exception as e:
    logger.info(f"Exception while calling LLM embed: {e}")

  try:
    with SessionLocal() as session:
      usage = Usage(
        provider="GEMINI",
        model = model,

        messages_sent = contents,
        tools_provided = [],
        response_received = response.model_dump(),

        tag = "embed_text",

        prompt_tokens = tokens_used,
        completion_tokens = 0,
        total_tokens = tokens_used
      )
      session.add(usage)
      session.commit()

  except Exception as e:
    logger.info(f"Exception while storing LLM call in database: {e}")

  return embedding_vector
