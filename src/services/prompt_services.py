from typing import Any

from repository.propmpt_repo import get_all_prompts


def get_prompts_service(db: any) -> list[Any]:
    records = get_all_prompts(db)
    return records
