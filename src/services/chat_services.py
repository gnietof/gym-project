import json
import logging

from ai_services.gemini import count, embed
from ai_services.groq import create
from ai_tools import tools_mapping, tools_schema
from repository.activity_repo import vector_search
from repository.propmpt_repo import get_prompt_by_tag
from repository.usage_repo import UsageScore, UsageTrack

LLAMA31_8B = "llama-3.1-8b-instant"
LLAMA33_70B = "llama-3.3-70b-versatile"
GPTOSS_20B = "openai/gpt-oss-20b"
GPTOSS_120B = "openai/gpt-oss-120b"


logger = logging.getLogger(__name__)


async def score_answer(track: str, mode: str, db: any):
    usage_score = UsageScore(db)
    usage_score.update_score(track, mode)


async def ask_agentic(id: str, question: str, db: any, model=GPTOSS_20B):
    """
    This is the agentic search version which includes both activities and scheduled sessions
    """

    usage_track = UsageTrack(db, id)

    prompt = get_prompt_by_tag(db, "gym_assistant")

    if not prompt:
        logger.warning("Prompt not found.")
        return ""

    messages = [
        {"role": "system", "content": prompt.template},
        {"role": "user", "content": question},
    ]

    loop_max = 10
    loop_count = 0
    run_loop = True
    final_answer = None
    final_track = None
    while run_loop and loop_count < loop_max:
        loop_count += 1

        response = create(messages, model, prompt.tag, tools_schema)
        track = usage_track.track_create(
            model,
            f"{prompt.tag}-{loop_count}",
            prompt.prompt,
            messages,
            tools_schema,
            response,
        )

        message = response.choices[0].message
        print(f"\nResponse: {message.content}")
        messages.append(message.model_dump(exclude={"annotations"}, exclude_none=True))

        if message.tool_calls:
            for tool_call in message.tool_calls:
                tool_name = tool_call.function.name
                tool_args = tool_call.function.arguments
                logger.info(f"\nTools: {tool_name}({tool_args})")

                target_tool = tools_mapping[tool_name]
                if target_tool:
                    tool_output = target_tool(db, id, model, tool_args)
                    print(f"\n{tool_output}")

                    messages.append(
                        {
                            "tool_call_id": tool_call.id,
                            "role": "tool",
                            "name": tool_name,
                            "content": json.dumps(tool_output),
                        }
                    )
                else:
                    logger.error(f"Tool {tool_name} is not available.")
        else:
            run_loop = False
            final_answer = message.content
            final_track = track

    return final_answer, final_track


async def ask_question(id: str, question: str, db: any, model=LLAMA31_8B) -> str:
    """
    This is the simple semantic search version. No longer used in the application.
    """

    usage_track = UsageTrack(db, id)

    # Question embedding. Counting tokens for usage tracking
    model = "gemini-embedding-001"
    tokens = count(question, model)
    response = embed(question, model)
    if not response:
        logger.error("Question embedding failed.")
        return "Sorry, could not find matching context for that question (embedding)."
    usage_track.track_embed(model, "embed_text", question, tokens, response)

    # Document search using the generated embedding
    query_vector = response.embeddings[0].values
    descriptions = vector_search(db, query_vector)
    if not descriptions:
        logger.warning("Search did not return any documents.")
        return "Sorry, could not find matching context for that question (search)."

    # Build context with retrieved documents
    context = [description.full_description for description in descriptions]
    full_context = "\n\n---\n\n".join(context)

    tag = "gym_assistant"
    prompt = get_prompt_by_tag(db, tag)
    if not prompt:
        logger.warning("Prompt not found.")
        return ""

    template = prompt.template.format(context=full_context)

    messages = [
        {"role": "system", "content": template},
        {"role": "user", "content": question},
    ]

    # Generate the response using the LLM
    response = create(messages, model, tag, [])
    track = usage_track.track_create(
        model, prompt.tag, prompt.prompt, messages, [], response
    )

    answer = response.choices[0].message.content

    return answer, track
