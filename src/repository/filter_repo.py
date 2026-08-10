from sqlalchemy import select

from schemas.filters import Category, Intensity, Subcategory


def get_all_categories(db: any) -> list[Category]:
    query = select(Category).order_by(Category.category)

    records = db.scalars(query).all()
    return records


def get_all_subcategories(db: any, category: str) -> list[Subcategory]:
    query = (
        select(Subcategory)
        .where(Subcategory.category == category)
        .order_by(Subcategory.subcategory)
    )

    records = db.scalars(query).all()
    return records


def get_all_intensities(db: any) -> list[Intensity]:
    query = select(Intensity).order_by(Intensity.description)

    records = db.scalars(query).all()
    return records
