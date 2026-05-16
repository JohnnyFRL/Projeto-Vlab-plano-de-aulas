from app.extensions import db
from app.models.lesson_plan import LessonPlan


def get_all():
    return LessonPlan.query.order_by(LessonPlan.created_at.desc()).all()


def get_by_id(plan_id):
    return LessonPlan.query.get(plan_id)


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
    for field in ("title", "objective", "summary", "planned_date", "discipline", "contents", "support_resources", "tags"):
        if field in data:
            setattr(plan, field, data[field])
    db.session.commit()
    return plan


def delete(plan):
    db.session.delete(plan)
    db.session.commit()
