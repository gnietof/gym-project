from ai_tools.gym_activities import retrieve_gym_activities
from ai_tools.gym_sessions import retrieve_gym_sessions

tools_mapping = {
    "gym_activities": retrieve_gym_activities,
    "gym_schedule": retrieve_gym_sessions,
}

tools_schema = [
    {
        "type": "function",
        "function": {
            "name": "gym_activities",
            "description": "Performs RAG to retrieve contextual informational documents and definitions regarding what specific gym activities entail.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The search keywords or descriptions outlining a type of exercise or activity.",
                    }
                },
                "required": ["query"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "gym_schedule",
            "description": "Retrieves timetable and specific days for activities. Automatically converts natural language query requests to target SQL expressions internally.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The scheduling request details indicating timestamps, activity targets, or days of interest.",
                    }
                },
                "required": ["query"],
            },
        },
    },
]
