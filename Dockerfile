FROM python:3.11-slim

RUN apt-get update && apt-get install -y git openssh-client && rm -rf /var/lib/apt/lists/*

RUN mkdir -p -m 0700 ~/.ssh && ssh-keyscan github.com >> ~/.ssh/known_hosts

WORKDIR /code

ARG REPO_URL="git@github.com:gnietof/gym-project.git"

ARG CACHE_BUST
RUN --mount=type=ssh git clone $REPO_URL .

RUN pip install --no-cache-dir -r requirements.txt

ENV PYTHONPATH=/code/src

EXPOSE 8000
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]