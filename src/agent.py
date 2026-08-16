import asyncio
import json
import logging

from ai_services.groq import create
from ai_tools import tools_mapping, tools_schema

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


async def ask_assistant(question: str, evaluation=False) -> str:

    # tools_schema = [
    #     {
    #         "type": "function",
    #         "function": {
    #             "name": "gym_activities",
    #             "description": "Performs RAG to retrieve contextual informational documents and definitions regarding what specific gym activities entail.",
    #             "parameters": {
    #                 "type": "object",
    #                 "properties": {
    #                     "query": {
    #                         "type": "string",
    #                         "description": "The search keywords or descriptions outlining a type of exercise or activity.",
    #                     }
    #                 },
    #                 "required": ["query"],
    #             },
    #         },
    #     },
    #     {
    #         "type": "function",
    #         "function": {
    #             "name": "gym_schedule",
    #             "description": "Retrieves timetable entries, rooms, and specific days for classes. Automatically converts natural language query requests to target SQL expressions internally.",
    #             "parameters": {
    #                 "type": "object",
    #                 "properties": {
    #                     "query": {
    #                         "type": "string",
    #                         "description": "The scheduling request details indicating timestamps, activity targets, or days of interest.",
    #                     }
    #                 },
    #                 "required": ["query"],
    #             },
    #         },
    #     },
    # ]

    # system_prompt = """
    #   You are an expert PostgreSQL generator. Your sole task is to turn user requests into a single executable SQL query for the GYM.VW_SESSIONS table.

    #   CRITICAL RULES:
    #   1. Always include the DOW (Day of Week) and TIME columns in the SELECT clause so the user knows exactly when the activity happens.
    #   2. Return ONLY the raw SQL query string. Do NOT wrap it in markdown code blocks (```sql), do NOT use surrounding quotes, and do NOT include any conversational filler.

    #   TABLE SCHEMA:
    #   Table: GYM.VW_SESSIONS
    #   - ACTIVITY_NAME (VARCHAR): Name of the fitness activity/class.
    #   - TIME (VARCHAR): Scheduled time in 'HH:MM' 24-hour format (e.g., '18:30').
    #   - DOW (VARCHAR): Day of the week. [Specify your format here, e.g., Full name 'Monday', or abbreviation 'Mon', or integer 1-7].
    #   - DURATION (INT): Duration of the activity in minutes.

    #   EXAMPLE OUPUT:
    #   SELECT ACTIVITY_NAME, DOW, TIME, DURATION FROM GYM.VW_SESSIONS WHERE LOWER(ACTIVITY_NAME) LIKE '%yoga%'
    # """

    # messages = [
    #     {"role": "system", "content": system_prompt},
    #     {"role": "user", "content": question},
    # ]

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

    # query = create(messages, model, "gym_schedule", [])
    # sql = text(query.choices[0].message.content.replace("```", ""))

    # print(f"\n{sql}")

    # with SessionLocal() as db:
    #     result = db.execute(sql)
    #     rows_as_dicts = [dict(row) for row in result.mappings()]
    #     schedule = json.dumps(rows_as_dicts, default=str)

    # print(f"\n{schedule}")

    # system_prompt2 = (
    #     "You are an expert Gym Assistant."
    #     "Using the provided schedule information answer questions about when activities."
    #     "are scheduled."
    #     f"--- START CONTEXT ---\n{schedule}\n--- END CONTEXT ---"
    # )

    # # system_prompt2.format(result=result)

    # messages2 = [
    #     {"role": "system", "content": system_prompt2},
    #     {"role": "user", "content": question},
    # ]

    # # model2 = "llama-3.1-8b-instant"
    # model2 = "llama-3.3-70b-versatile"

    # answer = create(messages2, model2, "gym_schedule2", [])

    # print(f"\n{answer.choices[0].message.content}")


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
