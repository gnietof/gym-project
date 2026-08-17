from typing import Any

from repository.filter_repo import (
    get_all_categories,
    get_all_intensities,
    get_all_subcategories,
)


def get_categories_service(db: any) -> list[Any]:
    records = get_all_categories(db)
    return records


def get_subcategories_service(db: any, category: str) -> list[Any]:
    records = get_all_subcategories(db)
    return records


def get_intensities_service(db: any) -> list[Any]:
    records = get_all_intensities(db)
    return records
