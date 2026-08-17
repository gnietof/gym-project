"""
This is an old piece of code I created when developing the agentic AI.
"""

import asyncio
import json
import logging

from ai_services.groq import create
from ai_tools import tools_mapping, tools_schema

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


async def ask_assistant(question: str, evaluation=False) -> str:

    messages = [
        {
            "role": "system",
            "content": (
                "You are an intelligent Gym Operations Assistant. You have access to two tools: "
                "1) 'gym_activities' to understand activity details using RAG, and "
                "2) 'gym_schedule' to fetch timetable sessions from SQL. "
                "If a user asks about what an activity is, use the RAG tool. If they ask when or where "
                "something occurs, use the SQL schedule tool. Combine tools if they ask about both."
                "When answering questions that require filtering by a trait (e.g., 'strength', 'cardio'), "
                "follow this strict workflow:"
                "1) Call the RAG tool first to identify which activity names match the requested trait."
                "2) Carefully read the text returned by the RAG tool and extract ONLY the exact names of those activities."
                "3) Pass those extracted activity names—and nothing else—to the schedule tool. Do not pass descriptions, "
                "sentences, or conversational filler into the schedule tool parameters."
                "If you do not know the answer say 'I do not know'."
                "Do not search the Internet."
            ),
        },
        {"role": "user", "content": question},
    ]

    # model = "llama-3.1-8b-instant"
    # model = "llama-3.3-70b-versatile"
    model = "openai/gpt-oss-20b"

    max_iterations = 5

    loopCount = 0
    runLoop = True
    final_content = None

    while runLoop and loopCount < max_iterations:
        loopCount += 1

        response = create(messages, model, "gym_schedule", tools_schema)

        message = response.choices[0].message
        print(f"\nResponse: {message.content}")
        messages.append(message)

        if message.tool_calls:
            for tool_call in message.tool_calls:
                logger.info(
                    f"\nTools: {tool_call.function.name}({tool_call.function.arguments})"
                )
                tool_name = tool_call.function.name
                tool_args = tool_call.function.arguments

                target_tool = tools_mapping[tool_name]

                if target_tool:
                    tool_output = target_tool(tool_args)
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
            runLoop = False
            final_content = message.content

    print(f"\nFinal response: {final_content}")


# asyncio.run(ask_assistant("When can I practice Zumba? Please include day and time."))
# asyncio.run(ask_assistant("¿Cuando hay clases de Bodypump? Incluye dia y hora."))

# asyncio.run(ask_assistant("Which activities are good for increasing strength."))

# asyncio.run(ask_assistant("¿Cuando son las actividades para incrementar la fuerza? "))

# asyncio.run(ask_assistant("¿Cuando son las actividades para incrementar la fuerza? "))

# asyncio.run(ask_assistant("Is there any yoga activity between 07:00 to 9:00? "))

asyncio.run(
    ask_assistant(
        "Which activities can I practice  to increase strength? When are those scheduled? "
    )
)
