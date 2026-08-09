from sqlalchemy import select, text

from dto.filters import CategoryDTO, IntensityDTO, SubcategoryDTO
from model.filters import Category, Intensity, Subcategory


def get_categories(db: any) -> list[Category]:
  query = (select(Category)
    .order_by(Category.category))

  records = db.scalars(query).all()
  return [CategoryDTO.model_validate(record) for record in records]

def get_subcategories(db: any,category: str) -> list[Subcategory]:
  query = (select(Subcategory)
    .where(Subcategory.category==category)
    .order_by(Subcategory.subcategory))

  records = db.scalars(query).all()
  return [SubcategoryDTO.model_validate(record) for record in records]

def get_intensities(db: any) -> list[Intensity]:
  query = (select(Intensity)
    .order_by(Intensity.description))

  records = db.scalars(query).all()
  return [IntensityDTO.model_validate(record) for record in records]


