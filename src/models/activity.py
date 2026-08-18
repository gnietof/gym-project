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


class GymLevelDTO(SQLModel):
    value: int
    description: str


# class IntensityDTO(SQLModel):
class IntensityDTO(GymLevelDTO):
    """Represents the description of the intensity of a gym activity"""


class SKillDTO(GymLevelDTO):
    """Represents the description of the intensity of a gym activity"""


class ImpactDTO(GymLevelDTO):
    """Represents the description of the intensity of a gym activity"""


class CaloricBurnDTO(GymLevelDTO):
    """Represents the description of the intensity of a gym activity"""


# class ActivityDTO(SQLModel):
class ActivityDTO(SQLModel):
    """Represents the description of a gym activity"""

    activity_name: str
    category: str
    subcategory: str
    intensity_level: str
    weights_used: str
    skill_level: str
    impact_level: str
    caloric_burn: str
