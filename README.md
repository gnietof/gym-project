# Gym Assistant
While other gym assistants focus on the proper way of performing different activities, this one on the other hand is focused on guiding the user to know more about each of the available guided activities.

## Demo

*** Work in progress ***

## Problem
When a user first joins a gym, such as the one this project is focused on, which offers more than 50 different guided activities, it is complex to understand which are the characteristics, the benefits (or contraindications) or the objectives for each of them. On top of this, the gym has a schedule with up to 250 weekly slots which change over time.

So, this assystant helps with knowing the details about each activity. Additionally, if required, finds the information in the schedule for the selected activities.

## Quickstart
This application has been prepared to be deployed using Docker Compose.

### Prerequisites
- Docker and Docker Compose
- A Gemini Key (Gemini is being used for the embeddings)
- A Groq Key (Groq is being used for AI agents and RAG)
  
### Full Setup

*** Work in progress ***

## Evaluation

### Retrieval Evaluation

*** Work in progress ***

### RAG Evaluation

*** Work in progress ***

## Architecture

*** Work in progress ***

## Prompts
Instead of hardcoding the prompt in the code or in a configuration file, they are being stored in a table in a database. Prompts can not be modified once stored but a new version can be created. 
Each tool has its own tag and LLM model. And each tag is associated to a different prompt. The idea is being able to use the most apropriate LLM for each task.

## Monitoring
A few views have been created to display the collected information.

### Expenses
Displays the token ussage. The different models used are included. There is no real cost displayed because free layers are being used.

### Performance
The user can evaluate the quality of the answer provided. This view provides information about the scoring. 

### Prompts
Each request sent by a user is stored in the database for audit purposes. The collected information includes timestamp, model, track (a unique id for each request), session (all the requests received as part a single conversation) and tokens used. The imput prompt and the response are also included.

## Future Improvements
### Prioritary
- Adding roles. Currently the tool is just prepared for a single user. The administrative views should not be available for an end user.
- Adding Grafana. The application collects information about each request received by the user: prompt, response, how many tokens where consumed ... This information is stored in a database and displayed using simple charts. Adding Grafana would improve data visualization.
### Secondary
- Providing a user interface to create version prompts from inside the tool
### Nice to have
- Being able to sort the tables.
