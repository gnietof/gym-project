from typing import Any

from repository.usage_repo import UsageRepo


def get_usages_service(db: any) -> list[Any]:
    usage_repo = UsageRepo(db)
    records = usage_repo.get_all_usages()
    return records


def get_scores_service(db: any) -> list[Any]:
    usage_repo = UsageRepo(db)
    records = usage_repo.get_all_scores()
    return records


def get_requests_service(db: any) -> list[Any]:
    usage_repo = UsageRepo(db)
    records = usage_repo.get_all_requests()
    return records


def get_request_by_track_service(db: any, track: str) -> Any:
    usage_repo = UsageRepo(db)
    record = usage_repo.get_request_by_track(track)
    return record
