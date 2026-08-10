from models.usage import RequestDTO, ScoreDTO, UsageDTO
from repository.usage_repo import get_all_requests, get_all_scores, get_all_usages


def get_usages_service(db: any) -> list[UsageDTO]:
    records = get_all_usages(db)
    return [UsageDTO.model_validate(record) for record in records]


def get_scores_service(db: any) -> list[ScoreDTO]:
    records = get_all_scores(db)
    return [ScoreDTO.model_validate(record) for record in records]


def get_requests_service(db: any) -> list[RequestDTO]:
    records = get_all_requests(db)
    return [RequestDTO.model_validate(record) for record in records]
