"""
This module includes the code required to do the Semantic Evaluation and the RAG evaluation.
A set of questions in the database are used.
Semantic Evaluation checks whether the retrieved documents using semantic (vector) search are the expected ones.
RAG evaluation checks if the answer created by the LLM is accurate.
"""

import json
import logging
import time

from sqlalchemy import select

from ai_services.gemini import embed
from ai_services.groq import create
from common.db.database import SessionLocal
from old_code.embed import semantic_search
from repository.activity_repo import vector_search
from repository.propmpt_repo import get_prompt_by_tag
from schemas.question import Question

logger = logging.getLogger(__name__)


async def retrieval_evaluation():
    # Retrieve questions from the database
    questions = get_questions()

    ok = {}
    for question in questions:
        documents = await semantic_search(question.question)
        print(f"{question.activity_name} -> {documents[0].activity_name}  ")
        for i, document in enumerate(documents):
            if question.activity_name == document.activity_name:
                print(f"\t{i}: {question.activity_name} -> {document.activity_name}  ")
                ok[i] = ok.get(i, 0) + 1

    for key, value in sorted(ok.items()):
        print(f"Matched {key}: {100 * value / len(questions):.2f}%")


LLAMA31_8B = "llama-3.1-8b-instant"
LLAMA33_70B = "llama-3.3-70b-versatile"
GPTOSS_20B = "openai/gpt-oss-20b"
GPTOSS_120B = "openai/gpt-oss-120b"


def rag_evaluation(model=LLAMA31_8B):
    # Retrieve questions from the database
    questions = get_questions()

    evaluations = []
    ok = {}
    # Evaluate each question
    for i, question in enumerate(questions):
        print(f"{i}: {question.question}")

        response = embed(question.question, "gemini-embedding-001")
        query_vector = response.embeddings[0].values

        with SessionLocal() as db:
            descriptions = vector_search(db, query_vector)
        context = [description.full_description for description in descriptions]
        full_context = "\n\n---\n\n".join(context)

        prompt = get_prompt_by_tag(db, "gym_activities_create")
        template = prompt.template.format(context=full_context)

        messages = [
            {"role": "system", "content": template},
            {"role": "user", "content": question.question},
        ]

        # Build the LLM answer to the question
        response = create(messages, model, "gym_schedule", [])
        answer = response.choices[0].message.content

        eval_prompt = (
            "You are an expert AI evaluation assistant. Your job is to validate answers to questions."
            "You will be provided with a question and its answer and must judge if the answer is"
            "accurately answering the question just based on the provided context."
            "Just provide a JSON (plain JSON do not include markdown annotations) including two fields:"
            "- evaluation: POSITIVE if the answer is correct, NEGATIVE if it is not accurate or MEDIUM if it is not fully correct. "
            "- arguments: Reasoning behind that evaluation. "
            f"QUESTION---\n{question}\n"
            f"CONTEXT---\n{full_context}\n"
            f"ANSWER---\n{answer}\n--- "
        )

        messages = [{"role": "system", "content": eval_prompt}]

        # Build the LLM evaluation to the question
        response2 = create(messages, "llama-3.1-8b-instant", "gym_assistant_eval", [])
        evaluation = json.loads(response2.choices[0].message.content)

        result = evaluation["evaluation"]
        evaluations.append(
            {
                "question": question.question,
                "answer": answer,
                "evaluation": result,
                "arguments": evaluation["arguments"],
            }
        )
        ok[result] = ok.get(result, 0) + 1

        time.sleep(1)

    with open(
        f"evaluations/RAG_{model.replace('/', '_')}.json", "w", encoding="utf-8"
    ) as file:
        json.dump(evaluations, file, indent=2)

    for key, value in sorted(ok.items()):
        print(f"Matched {key}: {100 * value / len(questions):.2f}%")


def get_questions() -> list[Question]:
    """
    Retrieve the list of test questions from the datbase
    """
    with SessionLocal() as db:
        query = select(Question)
        result = db.execute(query)

        questions = result.scalars().all()
        return questions


# asyncio.run(retrieval_evaluation())
rag_evaluation(model=LLAMA31_8B)
