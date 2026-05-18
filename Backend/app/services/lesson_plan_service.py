from datetime import date

from app.repositories import lesson_plan_repository as repo
from app.utils.logger import get_logger

logger = get_logger(__name__)


def list_plans(page, limit, search, discipline, tag, planned_date, sort):
    try:
        parsed_date = date.fromisoformat(planned_date) if planned_date else None
    except ValueError:
        parsed_date = None

    pagination = repo.get_all(
        page=page,
        limit=limit,
        search=search,
        discipline=discipline,
        tag=tag,
        planned_date=parsed_date,
        sort=sort,
    )

    return {
        "data": [p.to_dict() for p in pagination.items],
        "total": pagination.total,
        "page": pagination.page,
        "pages": pagination.pages,
        "per_page": pagination.per_page,
    }


def get_plan(plan_id):
    plan = repo.get_by_id(plan_id)
    return plan.to_dict() if plan else None


def create_plan(data):
    plan = repo.create(data)
    logger.info("Lesson plan created successfully: id=%s title=%r", plan.id, plan.title)
    return plan.to_dict()


def update_plan(plan_id, data):
    plan = repo.get_by_id(plan_id)
    if plan is None:
        return None
    updated = repo.update(plan, data)
    logger.info("Lesson plan updated successfully: id=%s", plan_id)
    return updated.to_dict()


def delete_plan(plan_id):
    plan = repo.get_by_id(plan_id)
    if plan is None:
        return False
    repo.delete(plan)
    logger.info("Lesson plan deleted successfully: id=%s", plan_id)
    return True
