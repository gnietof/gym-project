from models.filters import CategoryDTO, IntensityDTO, SubcategoryDTO
from repository.filter_repo import (
    get_all_categories,
    get_all_intensities,
    get_all_subcategories,
)


def get_categories_service(db: any) -> list[CategoryDTO]:
    records = get_all_categories(db)
    return [CategoryDTO.model_validate(record) for record in records]


def get_subcategories_service(db: any, category: str) -> list[SubcategoryDTO]:
    records = get_all_subcategories(db)

    return [SubcategoryDTO.model_validate(record) for record in records]


def get_intensities_service(db: any) -> list[IntensityDTO]:
    records = get_all_intensities(db)
    return [IntensityDTO.model_validate(record) for record in records]
