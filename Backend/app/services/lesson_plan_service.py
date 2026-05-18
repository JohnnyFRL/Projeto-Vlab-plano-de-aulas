from datetime import date

from app.repositories import lesson_plan_repository as repo


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
    return plan.to_dict()


def update_plan(plan_id, data):
    plan = repo.get_by_id(plan_id)
    if plan is None:
        return None
    return repo.update(plan, data).to_dict()


def delete_plan(plan_id):
    plan = repo.get_by_id(plan_id)
    if plan is None:
        return False
    repo.delete(plan)
    return True
