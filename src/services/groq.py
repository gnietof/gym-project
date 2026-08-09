""" Groq Helper
Helper module to centralize the access to Groq calls so that they are also tracked
"""

from common.ai.clients import get_groq_client
from common.db.dependencies import SessionLocal
from model.usage import Usage
from config_log import logger

groq_client = get_groq_client()

def create(messages: list[dict],model: str,tag= "",tools = []) -> any: 
  try: 
    response = groq_client.chat.completions.create(
      messages = messages,
      model = model,
      tools = tools,
      temperature = 0.2
    )
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

  except Exception as e:
    logger.info(f"Exception while storing LLM call in database: {e}")

  return response.choices[0].message.content

