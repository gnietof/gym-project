""" Groq Helper
Helper module to centralize the access to Groq calls so that they are also tracked
"""

import logging

from common.ai.clients import get_groq_client
from common.db.dependencies import SessionLocal
from model.usage import Usage

logger = logging.getLogger(__name__)

groq_client = get_groq_client()

def create(messages: list[dict],model: str,tag= "",tools = []) -> any: 
  try: 
    response = groq_client.chat.completions.create(
      messages = messages,
      model = model,
      tools = tools,
      temperature = 0.2
    )

    answer = response.choices[0].message.content
  except Exception as e:
    logger.info(f"Exception while calling LLM create: {e}")

  try:
    with SessionLocal() as session:
      usage = Usage(
        provider="GROQ",
        model = model,

        messages_sent = messages,
        tools_provided = tools,
        response_received = response.model_dump(),

        tag = tag,

        prompt_tokens = response.usage.prompt_tokens,
        completion_tokens = response.usage.completion_tokens,
        total_tokens = response.usage.total_tokens
      )
      session.add(usage)
      session.commit()
      session.refresh(usage)

      track = usage.track

  except Exception as e:
    logger.info(f"Exception while storing LLM call in database: {e}")

  return answer,track

