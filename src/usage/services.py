from sqlalchemy import select

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

