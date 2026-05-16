from app.repositories import lesson_plan_repository as repo


def list_plans():
    plans = repo.get_all()
    return [p.to_dict() for p in plans]


def get_plan(plan_id):
    plan = repo.get_by_id(plan_id)
    if plan is None:
        return None
    return plan.to_dict()


def create_plan(data):
    plan = repo.create(data)
    return plan.to_dict()


def update_plan(plan_id, data):
    plan = repo.get_by_id(plan_id)
    if plan is None:
        return None
    updated = repo.update(plan, data)
    return updated.to_dict()


def delete_plan(plan_id):
    plan = repo.get_by_id(plan_id)
    if plan is None:
        return False
    repo.delete(plan)
    return True
