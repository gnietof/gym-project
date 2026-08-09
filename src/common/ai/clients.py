import os
from dotenv import load_dotenv
from google import genai
from openai import OpenAI

load_dotenv()

def get_groq_client() -> any:

  key = os.getenv("GROQ_API_KEY")

  openai_client = OpenAI(
      api_key=os.getenv("GROQ_API_KEY"),
      base_url="https://api.groq.com/openai/v1"
  )

  return openai_client

def get_gemini_client() -> any:
  ai_client = genai.Client()

  return ai_client


