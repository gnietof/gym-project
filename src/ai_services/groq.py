"""Groq Helper
Helper module to centralize the access to Groq calls so that they are also tracked
"""

import logging
import os

from groq import APIConnectionError, APIStatusError
from openai import OpenAI

logger = logging.getLogger(__name__)

_groq_client: OpenAI | None = None


def get_groq_client() -> OpenAI:

    global _groq_client

    if _groq_client is None:
        _groq_client = OpenAI(
            api_key=os.getenv("GROQ_API_KEY"), base_url="https://api.groq.com/openai/v1"
        )

    return _groq_client


def create(messages: list[dict], model: str, tag: str, tools=None) -> any:
    if tools == None:
        tools = []

    client = get_groq_client()

    try:
        response = client.chat.completions.create(
            messages=messages, model=model, tools=tools, temperature=0.2
        )
        # answer = response.choices[0].message.content
    except APIConnectionError as e:
        logger.info(f"Exception while connecting with Groq: {e}")
    except APIStatusError as e:
        logger.info(f"Exception while calling Groq: {e}")

    return response
