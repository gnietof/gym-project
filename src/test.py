from dotenv import load_dotenv
from openai import OpenAI
import os

load_dotenv()

key = os.getenv("GROQ_API_KEY")

print(f"Key: {key}")

openai_client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)

def classify_question(instructions:str, questions:str) -> str:
  # model = "llama-3.1-8b-instant"
  # model = "llama-3.3-70b-versatile"
  model = "qwen/qwen3.6-27b"
  # model = "meta-llama/llama-prompt-guard-2-22m"

  messages = [
    {"role":"system","content":instructions},
    {"role":"user","content":question}
  ]

  response = openai_client.chat.completions.create(
      model=model,
      messages=messages,
  )

  json = response.choices[0].message.content
  print(f"\nQuestion: {question}\nSchema: {json}\n")
  print(f"\nInput: {response.usage.prompt_tokens}\nOutput: {response.usage.completion_tokens}\n")

  return json


instructions = """
You are a gym assistant. You are NOT describing an activity. 
You are extracting search contraints from the user's request.
Every property in the JSON represents a constraint the user explicitly requested or that can be confidently inferred.

Schema:

activity_name: name of the activity
category: category of the activity
sub_category: subcategory of the activity
description: text describing the activity
intensity_level: an array with possible intensity values (Low, Medium, High or Extreme)
target_age_group: an age range
weights_used: whether weights are being used or not (true or false)
primary_benefit: text describing the main benefit of this activity
skill_level: an array with possible skill values (Low, Medium, High)
impact_level: an array with possible impact values (No, Low, Medium, High)
social_dynamic: an array with possible social values (Solo, Group, Partner)
caloric_burn: an array with possible caloric values (Low, Medium, High, Very High)
mental_focus: text describing the mental focus
contraindications: text describing possible contraindications 
interesting_fact: text describing an interesing fact

Just provide the JSON schema. No comments, explanations or disclaimers.
Fill the properties in the JSON schema based on the user question. Do NOT add other content.
If the user did not mention a constraint, omit it.
If a property is free text (description, primary_benefit, mental_focus, contraindications, interesting fact), 
copy or summarize ONLY the concept requested by the user.

"""

# question = "I am looking for a beginner activity with moderate intensity that improves posture and is easy on the joints."
# json = classify_question(instructions, question)

# question = "Find me an activity wich has high intensity and is practiced in groups but having low complexity."
# json = classify_question(instructions, question)

# question = "Are there any activities related with cycling?."
# json = classify_question(instructions, question)

question = "Are there any aerobic activities?."
json = classify_question(instructions, question)


