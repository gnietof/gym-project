from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from common.db.dependencies import get_db
from models.activity import ActivityDTO, CategoryDTO, IntensityDTO, SubcategoryDTO
from services.activity_services import (
    get_activities_service,
    get_categories_service,
    get_intensities_service,
    get_subcategories_service,
)

router = APIRouter()


@router.get("/categories", response_model=list[CategoryDTO])
def get_categories_endpoint(db: Session = Depends(get_db)):
    records = get_categories_service(db)
    return [CategoryDTO.model_validate(record) for record in records]


@router.get("/subcategories/{category}", response_model=list[SubcategoryDTO])
def get_subcategories_endpoint(category: str, db: Session = Depends(get_db)):
    records = get_subcategories_service(db, category)
    return [SubcategoryDTO.model_validate(record) for record in records]


@router.get("/intensities", response_model=list[IntensityDTO])
def get_intensities_endpoint(db: Session = Depends(get_db)):
    records = get_intensities_service(db)
    return [IntensityDTO.model_validate(record) for record in records]


@router.get("/activities", response_model=list[ActivityDTO])
def get_activities_endpoint(db: Session = Depends(get_db)):
    records = get_activities_service(db)
    return [ActivityDTO.model_validate(record) for record in records]
