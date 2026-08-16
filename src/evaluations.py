import asyncio
import logging

from sqlalchemy import select

from ai_services.gemini import embed
from common.db.database import SessionLocal
from schemas.activity import Activity
from schemas.question import Question

logger = logging.getLogger(__name__)


async def retrieval_evaluation():
    with SessionLocal() as db:
        query = select(Question)
        result = db.execute(query)

        questions = result.scalars().all()

    ok = {}
    for question in questions:
        documents = await semantic_search(question.question, 5)
        print(f"{question.activity_name} -> {documents[0].activity_name}  ")
        for i, document in enumerate(documents):
            if question.activity_name == document.activity_name:
                print(f"\t{i}: {question.activity_name} -> {document.activity_name}  ")
                ok[i] = ok.get(i, 0) + 1

    for key, value in sorted(ok.items()):
        print(f"Matched {key}: {100 * value / len(questions):.2f}%")


async def semantic_search(question: str, limit: int = 5) -> list[Activity]:

    model = "gemini-embedding-001"

    query_vector = embed(question, model)

    query = (
        select(Activity)
        .order_by(Activity.embedding.cosine_distance(query_vector.embeddings[0].values))
        .limit(limit)
    )

    with SessionLocal() as db:
        result = db.execute(query)
        closest = result.scalars().all()

    return closest


asyncio.run(retrieval_evaluation())
