from sqlalchemy import asc, desc, or_

from app.extensions import db
from app.models.lesson_plan import LessonPlan


# ─── leitura simples ────────────────────────────────────────────────────────

def get_by_id(plan_id: int):
    return db.session.get(LessonPlan, plan_id)


# ─── listagem com filtros e paginação ────────────────────────────────────────

_SORT_MAP = {
    "title": LessonPlan.title,
    "created_at": LessonPlan.created_at,
    "planned_date": LessonPlan.planned_date,
}


def get_all(
    page: int = 1,
    per_page: int = 10,
    search: str = "",
    discipline: str = "",
    tags: str = "",
    date_from=None,
    date_to=None,
    sort_by: str = "created_at",
    order: str = "desc",
):
    """
    Retorna uma página de planos com suporte a:
      - search        → busca por título (ILIKE)
      - discipline    → filtro por disciplina (ILIKE)
      - tags          → string CSV; qualquer tag presente (OR)
      - date_from/to  → intervalo de planned_date
      - sort_by       → title | created_at | planned_date
      - order         → asc | desc
    """
    query = LessonPlan.query

    if search:
        query = query.filter(LessonPlan.title.ilike(f"%{search}%"))

    if discipline:
        query = query.filter(LessonPlan.discipline.ilike(f"%{discipline}%"))

    if tags:
        tag_list = [t.strip() for t in tags.split(",") if t.strip()]
        if tag_list:
            query = query.filter(or_(*[LessonPlan.tags.ilike(f"%{t}%") for t in tag_list]))

    if date_from:
        query = query.filter(LessonPlan.planned_date >= date_from)
    if date_to:
        query = query.filter(LessonPlan.planned_date <= date_to)

    sort_col = _SORT_MAP.get(sort_by, LessonPlan.created_at)
    sort_fn = desc if order.lower() == "desc" else asc
    query = query.order_by(sort_fn(sort_col))

    return query.paginate(page=page, per_page=per_page, error_out=False)


# ─── escrita ─────────────────────────────────────────────────────────────────

def create(data: dict) -> LessonPlan:
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


def update(plan: LessonPlan, data: dict) -> LessonPlan:
    for field in (
        "title", "objective", "summary", "planned_date",
        "discipline", "contents", "support_resources", "tags",
    ):
        if field in data:
            setattr(plan, field, data[field])
    db.session.commit()
    return plan


def delete(plan: LessonPlan) -> None:
    db.session.delete(plan)
    db.session.commit()
