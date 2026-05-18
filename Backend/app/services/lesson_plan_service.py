from datetime import date

from app.repositories import lesson_plan_repository as repo


def list_plans(
    page: int = 1,
    per_page: int = 10,
    search: str = "",
    discipline: str = "",
    tags: str = "",
    date_from=None,
    date_to=None,
    sort_by: str = "created_at",
    order: str = "desc",
) -> dict:
    pagination = repo.get_all(
        page=page,
        per_page=per_page,
        search=search,
        discipline=discipline,
        tags=tags,
        date_from=date_from,
        date_to=date_to,
        sort_by=sort_by,
        order=order,
    )
    return {
        "data": [p.to_dict() for p in pagination.items],
        "meta": {
            "page": pagination.page,
            "per_page": pagination.per_page,
            "total": pagination.total,
            "pages": pagination.pages,
            "has_next": pagination.has_next,
            "has_prev": pagination.has_prev,
        },
    }


def get_plan(plan_id: int):
    plan = repo.get_by_id(plan_id)
    return plan.to_dict() if plan else None


def create_plan(data: dict) -> dict:
    plan = repo.create(data)
    return plan.to_dict()


def update_plan(plan_id: int, data: dict):
    plan = repo.get_by_id(plan_id)
    if plan is None:
        return None
    return repo.update(plan, data).to_dict()


def delete_plan(plan_id: int) -> bool:
    plan = repo.get_by_id(plan_id)
    if plan is None:
        return False
    repo.delete(plan)
    return True
