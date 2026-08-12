from typing import Any

from repository.usage_repo import (
    get_all_requests,
    get_all_scores,
    get_all_usages,
    get_request_by_track,
)


def get_usages_service(db: any) -> list[Any]:
    records = get_all_usages(db)
    return records


def get_scores_service(db: any) -> list[Any]:
    records = get_all_scores(db)
    return records


def get_requests_service(db: any) -> list[Any]:
    records = get_all_requests(db)
    return records


def get_request_by_track_service(track: str, db: any) -> Any:
    record = get_request_by_track(db, track)
    return record
