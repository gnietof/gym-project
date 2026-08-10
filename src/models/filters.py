from sqlmodel import SQLModel


class CategoryDTO(SQLModel):
    """Represents the description of a gym activity category"""

    id: int
    category: str


class SubcategoryDTO(SQLModel):
    """Represents the description of a gym activity subcategory"""

    id: int
    category: int
    subcategory: str


class IntensityDTO(SQLModel):
    """Represents the description of the intensity of a gym activity"""

    value: int
    description: str
