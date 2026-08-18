from sqlalchemy import case, select

from schemas.activity import (
    Activity,
    CaloricBurn,
    Category,
    Impact,
    Intensity,
    Skill,
    Subcategory,
)


def get_all_activities(db: any) -> list[Activity]:
    query = (
        select(
            Activity.activity_name,
            Category.category.label("category"),
            Subcategory.subcategory.label("subcategory"),
            Intensity.description.label("intensity_level"),
            case((Activity.weights_used == True, "Yes"), else_="No").label(
                "weights_used"
            ),
            Skill.description.label("skill_level"),
            Impact.description.label("impact_level"),
            CaloricBurn.description.label("caloric_burn"),
        )
        .join(Category, Activity.category_name)
        .join(Subcategory, Activity.subcategory_name)
        .join(Intensity, Activity.intensity_level_name)
        .join(Skill, Activity.skill_level_name)
        .join(Impact, Activity.impact_level_name)
        .join(CaloricBurn, Activity.caloric_burn_name)
    )
    activities = db.execute(query).all()

    return activities


def vector_search(db: any, query_vector: list[float], limit=5) -> list[Activity]:

    query = (
        select(Activity)
        .order_by(Activity.embedding.cosine_distance(query_vector))
        .limit(limit)
    )

    closest = db.scalars(query).all()

    return closest
