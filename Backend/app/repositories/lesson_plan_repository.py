from sqlalchemy import asc, desc

from app.extensions import db
from app.models.lesson_plan import LessonPlan

_SORT_FIELDS = {
    "title": LessonPlan.title,
    "created_at": LessonPlan.created_at,
    "planned_date": LessonPlan.planned_date,
}


def get_all(page, limit, search, discipline, tag, planned_date, sort):
    query = LessonPlan.query

    if search:
        query = query.filter(LessonPlan.title.ilike(f"%{search}%"))

    if discipline:
        query = query.filter(LessonPlan.discipline.ilike(f"%{discipline}%"))

    if tag:
        query = query.filter(LessonPlan.tags.ilike(f"%{tag}%"))

    if planned_date:
        query = query.filter(LessonPlan.planned_date == planned_date)

    sort_col = _SORT_FIELDS.get(sort, LessonPlan.created_at)
    query = query.order_by(desc(sort_col))

    return query.paginate(page=page, per_page=limit, error_out=False)


def get_by_id(plan_id):
    return db.session.get(LessonPlan, plan_id)


def create(data):
    plan = LessonPlan(
        title=data["title"],
        objective=data["objective"],
        summary=data["summary"],
        planned_date=data["planned_date"],
        discipline=data["discipline"],
        contents=data.get("contents"),
        support_resources=data.get("support_resources"),
        tags=data.get("tags"),
    )
    db.session.add(plan)
    db.session.commit()
    return plan


def update(plan, data):
    for field in ("title", "objective", "summary", "planned_date",
                  "discipline", "contents", "support_resources", "tags"):
        if field in data:
            setattr(plan, field, data[field])
    db.session.commit()
    return plan


def delete(plan):
    db.session.delete(plan)
    db.session.commit()
