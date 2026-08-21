"""
This module generates the embeddings for each of the activities.
"""

import logging

from sqlalchemy import select

from ai_services.gemini import embed
from common.db.database import SessionLocal
from schemas.activity import Embedding

logger = logging.getLogger(__name__)


def generate_emebddings():

    with SessionLocal() as db:
        query = select(Embedding).where(Embedding.embedding == None)
        result = db.execute(query)

        descriptions = result.scalars().all()

        if not descriptions:
            print("All activities already have embeddings")
            return

        updated_count = 0
        for description in descriptions:
            response = embed(description.content, "gemini-embedding-001")
            description.embedding = response.embeddings[0].values
            updated_count += 1

        db.commit()

    print(f"{updated_count} documents embedded.")


# async def semantic_search(question: str, limit: int = 5) -> list[Activity]:

#     model = "gemini-embedding-001"

#     query_vector = embed(question, model)

#     query = (
#         select(Activity)
#         .order_by(Activity.embedding.cosine_distance(query_vector))
#         .limit(limit)
#     )

#     with SessionLocal() as db:
#         result = db.execute(query)
#         closest = result.scalars().all()

#     return closest


# async def ask_assistant(question: str, evaluation=False) -> str:
#     descriptions = await semantic_search(question)

#     if not descriptions:
#         return "Sorry, could not find matching activities"

#     context = []
#     for description in descriptions:
#         context.append(description.full_description)

#     full_context = "\n\n---\n\n".join(context)

#     system_prompt = (
#         "You are an expert Gym and Fitness AI assistant. Your job is to answer user questions "
#         "accurately using ONLY the verified context provided below. If the answer cannot be "
#         "found in the context, politely state that you do not know."
#         "Do NOT add anything which is not in the infomration provided\n\n"
#         f"--- START CONTEXT ---\n{full_context}\n--- END CONTEXT ---"
#     )

#     messages = [
#         {"role": "system", "content": system_prompt},
#         {"role": "user", "content": question},
#     ]

#     model = "llama-3.1-8b-instant"

#     answer = create(messages, model, "gym_assistant", [])

#     if evaluation:
#         eval_prompt = (
#             "You are an expert AI evaluation assistant. Your job is to validate answers to questions."
#             "You will be provided with a question and its answer and must judge if the answer is"
#             "accurately answering the question just based on the provided context."
#             f"QUESTION---\n{question}\n"
#             f"CONTEXT---\n{full_context}\n"
#             f"ANSWER---\n{answer}\n--- "
#         )

#         messages = [{"role": "system", "content": eval_prompt}]

#         evaluation = create(messages, "llama-3.1-8b-instant", "gym_assistant_eval", [])

generate_emebddings()
