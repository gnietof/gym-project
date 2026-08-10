import asyncio
import logging

from sqlalchemy import select

from ai_services.gemini import embed
from ai_services.groq import create
from common.db.database import SessionLocal
from schemas.activity import Activity

logger = logging.getLogger(__name__)


async def generate_emebddings():

    with SessionLocal() as db:
        query = select(Activity).where(Activity.embedding == None)
        result = db.execute(query)

        activities = result.scalars().all()

        if not activities:
            print("All activities already have embeddings")

        updated_count = 0
        for activity in activities:
            activity.embedding = embed(activity.full_description)
            updated_count += 1

        db.commit()

    print(f"{updated_count} documents embedded.")


async def semantic_search(question: str, limit: int = 5) -> list[Activity]:

    query_vector = embed(question)

    query = (
        select(Activity)
        .order_by(Activity.embedding.cosine_distance(query_vector))
        .limit(limit)
    )

    with SessionLocal() as db:
        result = db.execute(query)
        closest = result.scalars().all()

    return closest


async def ask_assistant(question: str, evaluation=False) -> str:
    activities = await semantic_search(question)

    if not activities:
        return "Sorry, could not find matching activities"

    context = []
    for activity in activities:
        context.append(activity.full_description)

    full_context = "\n\n---\n\n".join(context)

    system_prompt = (
        "You are an expert Gym and Fitness AI assistant. Your job is to answer user questions "
        "accurately using ONLY the verified context provided below. If the answer cannot be "
        "found in the context, politely state that you do not know."
        "Do NOT add anything which is not in the infomration provided\n\n"
        f"--- START CONTEXT ---\n{full_context}\n--- END CONTEXT ---"
    )

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": question},
    ]

    model = "llama-3.1-8b-instant"

    answer = create(messages, model, "gym_assistant", [])

    if evaluation:
        eval_prompt = (
            "You are an expert AI evaluation assistant. Your job is to validate answers to questions."
            "You will be provided with a question and its answer and must judge if the answer is"
            "accurately answering the question just based on the provided context."
            f"QUESTION---\n{question}\n"
            f"CONTEXT---\n{full_context}\n"
            f"ANSWER---\n{answer}\n--- "
        )

        messages = [{"role": "system", "content": eval_prompt}]

        evaluation = create(messages, "llama-3.1-8b-instant", "gym_assistant_eval", [])


# asyncio.run(generate_emebddings())

# asyncio.run(semantic_search("I am looking for an activity which makes my muscles work continuosly"))
# asyncio.run(semantic_search("Which activities are not good for me if I have a back pain?"))
# asyncio.run(semantic_search("Which activities are similar to riding a bike?"))
# asyncio.run(semantic_search("Which activities are similar to aerobics?"))
# asyncio.run(semantic_search("Any activities being executed hanging from the ceiling?"))
# asyncio.run(semantic_search("¿Qué actividades hay similares a ir en bici?"))

# asyncio.run(ask_assistant("¿Qué actividades se practican por parejas?"))
# asyncio.run(ask_assistant("Which activities are similar to riding a bike?"))
# asyncio.run(ask_assistant("Is there any Yoga activity?"))
# asyncio.run(ask_assistant("Quiero hacer actividades que no sufra la espalda."))
# asyncio.run(ask_assistant("Cual es la receta de la tortilla francesa?"))
asyncio.run(ask_assistant("¿Qué actividades hay similares a ir en bici?"))
