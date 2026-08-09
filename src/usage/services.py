from sqlalchemy import select,func

from model.usage import Usage

def get_usage(db: any) -> list[Usage]:
  query = (
    select(
      Usage.timestamp,
      Usage.provider,
      Usage.model,
      Usage.prompt_tokens,
      Usage.completion_tokens,
      Usage.total_tokens
    )
    .order_by(Usage.timestamp.desc())
    # .limit(20)
  )

  records = db.execute(query)

  return records

def get_scores(db: any) -> list[any]:
  query = (
    select(
      Usage.model,
      func.count().filter(Usage.score=="U").label("up"),
      func.count().filter(Usage.score=="D").label("down")
    )
    .filter(Usage.provider=="GROQ")
    .group_by(Usage.model)
  )

  records = db.execute(query)

  return records

def get_requests(db: any) -> list[any]:
  query = (
    select(
      Usage.timestamp,
      Usage.model,
      Usage.track,
      Usage.prompt_tokens,
      Usage.completion_tokens,
      Usage.total_tokens,
      # Usage.score,
      func.coalesce(Usage.score, "").label("score")
    )
    .filter(Usage.provider=="GROQ")
    .order_by(Usage.timestamp.desc())
  )

  records = db.execute(query)

  return records

