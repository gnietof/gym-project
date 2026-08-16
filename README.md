# Gym Assistant
While other gym assistants focus on the proper way of performing different activities, this one on the other hand is focused on guiding the user to know more about each of the available guided activities.

Initially, this tool was only able to answer RAG question on a corpus of information about different guided activities in a gym. 
Then the tool was refactored so that an agent was evaluating the questions and tried to answer them by using two different tools: 
- gym_activities: this one is using RAG to extract information about activities.
- gym_sessions: up to 254 scheduled sessions for 51 different activities have been added to the database. In this case, the LLM writes the SQL queries to retrieve the required information.

Keyword search has not been used in this project. Many similar words are used to describe activities and the documents returned where not providing the right answers.

## Demo

*** Work in progress ***

**Note**: The tool has a 'WhatsApp-like' look because the interface is being migrated to WhatsApp. Although I have already 'migrated' other AI tools to WhatsApp, this is still a "work in progress" for this project.

<img width="1381" height="821" alt="image" src="https://github.com/user-attachments/assets/825cfcd8-d5f4-463d-b0f7-55f3b64dffdc" />

## Problem
When a user first joins a gym, such as the one this project is focused on, which offers more than 50 different guided activities, it is complex to understand which are the characteristics, the benefits (or contraindications) or the objectives for each of them. On top of this, the gym has a schedule with up to 250 weekly slots which change over time.

So, this assistant helps with knowing the details about each activity. Additionally, if required, finds the information in the schedule for the selected activities.

## Quickstart
This application has been prepared to be deployed using Docker Compose.

### Prerequisites
- Docker and Docker Compose
- A Gemini Key (Gemini is being used for the embeddings)
- A Groq Key (Groq is being used for AI agents and RAG)
  
### Full Setup
The application uses two containers, one for Postgres and another one for FastAPI.

The repository includes:
- The Dockerfile required to build the FastAPI container. The Dockerfile retrieves code directly from the Github repository. Small adjustments will be required to use a local replica.
- The doker-compose.yml which allows starting/stopping both containers in sync.
- A backup of the Postgres database which contains all the tables required. This backup is 'automagically' restored into Postgres first time the server is started.

Use this commands below for building and starting the containers. If directly accessing Github, the SSH keys for authentication should be available in ~/.ssh.
```bash
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_ed25519

env SSH_AUTH_SOCK=$SSH_AUTH_SOCK docker compose build --build-arg CACHE_BUST=$(date +%s) web 

docker compose up 

```

### Database
The Postgres database includes several tables:
| Schema | Table | Description |
|---|---|----|
| gym | activities | Description of each of the activities including the embedded vectors |
| gym | schedule | Schedule of each of the activities along the week |
| gym | questions | Questions used for evaluation |
| llm | prompts | The prompts which are used by the agent. |
| log | usage | This table stores each request which has been sent to the LLM's. The contents are then used for building the dashboards. |

Additional tables have been included (categories, subcategories, intensity, ...) for future use.

## Evaluation

### Retrieval Evaluation

A collection of 50+ questions where generated for different activities. Semantic search has been used. Keyword search provided poor results because of the many similar words used in each description.
Using semantic search for this set of questions the hit rate was 74%. Although 'wrong' answers are not really wrong. 

<details>
<summary>Output detail</summary>
For each question, five documents where retrieved using semantic search. If the expected activity was included in one of the returned documents it was included. Only if the first document matched the expected one was counted as a hit.  


| Expected | Returned | Found position? |
|----------|----------|----------|
| Antigravity Yoga | Antigravity Yoga | 0 | 
| Antigravity Yoga | Antigravity Yoga | 0 | 
| Antigravity Yoga | Antigravity Yoga | 0 | 
| Antigravity Yoga | Antigravity Yoga | 0 | 
| Antigravity Yoga | Antigravity Yoga | 0 | 
| Antigravity Yoga | Antigravity Yoga | 0 | 
| Bootcamp | Bootcamp | 0 | 
| Bootcamp | Team WOD | 2 | 
| Bootcamp | Cross Gym | 2 | 
| Bootcamp | Bootcamp | 0 | 
| Bootcamp | Team WOD | 1 | 
| Bootcamp | Bootcamp | 0 | 
| Bootcamp | Booster Keiser | -- |   
| Bootcamp | Cycling HIIT | 1 | 
| Bootcamp | Bootcamp | 0 | 
| Bootcamp | Bootcamp | 0 | 
| Cycling HIIT | Cycling HIIT | 0 | 
| Cycling HIIT | Cycling HIIT | 0 | 
| Cycling HIIT | Cycling HIIT | 0 | 
| Cycling HIIT | Cycling HIIT | 0 | 
| Elle Fitness | Elle Fitness | 0 | 
| Elle Fitness | Hybrid | 1 | 
| Elle Strong | Elle Strong | 0 | 
| Elle Strong | Antigravity Yoga | -- | 
| Hybrid | Hybrid | 0 | 
| Hybrid | Hybrid | 0 | 
| Hybrid | Hybrid | 0 | 
| Hybrid | Hybrid | 0 | 
| Hybrid | Hybrid | 0 | 
| Hybrid Max | Hybrid Max | 0 | 
| Hybrid Max | Hybrid | 1 | 
| Hyrox | Hyrox Force | -- | 
| Hyrox | Strongman | -- | 
| Inspired Ashtanga | Inspired Ashtanga | 0 | 
| Inspired Ashtanga | Pilates | -- |
| Pilates | Pilates | 0 | 
| Pilates | Inspired Ashtanga | -- |
| RCVRI | RCVRI | 0 | 
| RCVRI | RCVRI | 0 | 
| Rig | Rig | 0 | 
| Rig | Rig | 0 | 
| Strongman | Strongman | 0 | 
| Strongman | Strongman | 0 | 
| Yin Yan Yoga | Yin Yan Yoga | 0 | 
| Yin Yan Yoga | Yin Yan Yoga | 0 | 
| Zumba | Zumba | 0 | 
| Zumba | Zumba | 0 | 


Matched 0: 74.47%
Matched 1:  8.51%
Matched 2:  4.26%

</details>

### RAG Evaluation

*** Work in progress ***

## Architecture
The architecture consists basically of two pieces: a FastAPI to handle the user interface (including the reporting sections) and the Postgres database to store both the documents and the tracking information. 

The pgvector extension for Postgres has been used for simplicity. Instead of using Elasticsearch, Pinecode or any other, by using this extension, Postgres is capable of storing the embedding next to the documents and perform the semantic search.

<img width="841" height="581" alt="image" src="https://github.com/user-attachments/assets/81caf5b1-7e2c-431c-834a-7d801df05dae" />

The user interface has been created using plain HTML and Javascript. 
The communication with the backend server running on the FastAPI server is using a REST API with requests and responses using JSON. FastAPI listens on port 8000.
Finally, the backend is written in Python. The communication with the database is using SQLAlchemy.

### Agentic AI
Initially, this tool just used semantic search for finding those activities which matched the provided question.
Later a new table including the schedule of each activity in the gym was added to the database. 
So, the initial semantic search was refactored into a tool which was capable of retrieving documents.
A second tool was added which was capable of finding scheduled activities. This tool does not use semantic search. The LLM generates a SQL query which retrieves the required information from the database.  
<img width="533" height="312" alt="image" src="https://github.com/user-attachments/assets/95d22ea6-5579-4692-a2db-4bf2126cb3ba" />  
When a question arrives, the Agent checks which tool would be the most appropriate for returning the required information. If both are required, multiple tool calls are executed until the Agent has enough information to generate an answer.

## Monitoring
A few views have been created to display the collected information. Each LLM request is being registered in the database: timestamp, model, tag, tokens used ... The information is sent to a Postgres table. 
In the future this information might feed a tool like Langfuse or being monitored using Grafana.

### Expenses
Displays the token usage. The different models used are included. There is no real cost displayed because free layers are being used.

**Note**: On August 14th, I read about llama-3.3-70b-versatile being sunset in Groq and so I started testing with openai/gpt-oss-20b and openai/gpt-oss-120b models as can be seen on the screenshot.

<img width="1386" height="821" alt="image" src="https://github.com/user-attachments/assets/8b00cb31-bd4b-41aa-be68-120541ca2404" />

### Performance
The user can evaluate the quality of the answer provided. This view provides information about the scoring when users give feedback for the response provided.

<img width="1386" height="822" alt="image" src="https://github.com/user-attachments/assets/ae08e289-be04-4b68-a4f3-f330ac508e62" />

### Requests
Each request sent by a user is stored in the database for audit purposes. The collected information includes timestamp, model, track (a unique id for each request), session (all the requests received as part a single conversation) and tokens used. The input prompt and the response are also included.

The picture below shows a single session where the agent has executed three loops and called both tools. First gym_activities to know which activities match the request and then gym_sessions to provide the user with the schedule.

<img width="1387" height="318" alt="image" src="https://github.com/user-attachments/assets/39ff6b04-2856-43c1-844e-9da37a60252f" />

<img width="1386" height="302" alt="image" src="https://github.com/user-attachments/assets/44df0865-bb7a-4f04-a5a0-6bd5b2b2ecf6" />

A detail view shows all the messages sent and the response received for each LLM request. Any request which has been scored is highlighted in green or red.

<img width="1388" height="819" alt="image" src="https://github.com/user-attachments/assets/14af4df9-45f5-4212-8029-090256716971" />

### Prompts
Instead of hardcoding the prompt in the code or in a configuration file, they are being stored in a table in the database. Prompts can not be modified once stored but a new version can be created. 
Each tool has its own tag and LLM model. And each tag is associated to a different prompt. The idea is being able to use the most appropriate LLM for each task.

The tool is prepared to manage the prompts so they can be audited later. This part is a "work in progress" and currently the tool does not allow to version or activate/deactivate a prompt.

<img width="1387" height="380" alt="image" src="https://github.com/user-attachments/assets/e1f31722-4a5d-4909-ae3a-b37ecabd6e98" />

## Future Improvements
### Priority
- Adding 'memory'. While the application generates a session id, each question has no previous context. By storing previous messages in a conversation more complex conversations will be available.
- Using additional fields for each activity (intensity, difficulty, use of weights ...) to further refine the search of the activities. 
- Adding roles. Currently the tool is just prepared for a single user. The administrative views should not be available for an end user.
- Adding Grafana. The application collects information about each request received by the user: prompt, response, how many tokens where consumed ... This information is stored in a database and displayed using simple charts. Adding Grafana would improve data visualisation.
### Secondary
- Providing a user interface to create version prompts from inside the tool
### Nice to have
- Being able to sort/filter the tables using different criteria.
 
