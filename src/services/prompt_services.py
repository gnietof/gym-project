from models.prompt import PromptDTO
from repository.propmpt_repo import get_all_prompts


def get_prompts_service(db: any) -> list[PromptDTO]:
    records = get_all_prompts(db)
    return [PromptDTO.model_validate(record) for record in records]
