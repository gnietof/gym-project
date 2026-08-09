from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from common.db.dependencies import get_db
from dto.filters import CategoryDTO, IntensityDTO, SubcategoryDTO
from filter.services import get_categories, get_subcategories, get_intensities

router = APIRouter()

@router.get("/categories", response_model=list[CategoryDTO])
def categories(db: Session = Depends(get_db)):
  records = get_categories(db)
  return [CategoryDTO.model_validate(record) for record in records]

@router.get("/subcategories/{category}", response_model=list[SubcategoryDTO])
def subcategories(category: str, db: Session = Depends(get_db)):
  records = get_subcategories(db,category)
  return [SubcategoryDTO.model_validate(record) for record in records]

@router.get("/intensities", response_model=list[IntensityDTO])
def intensities(db: Session = Depends(get_db)):
  records  = get_intensities(db)
  return [IntensityDTO.model_validate(record) for record in records]



