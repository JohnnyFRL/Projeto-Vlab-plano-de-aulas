import logging
from datetime import date

from flask import request, jsonify
from marshmallow import ValidationError

from app.schemas.lesson_plan_schema import LessonPlanSchema, LessonPlanUpdateSchema
from app.services import lesson_plan_service as service

logger = logging.getLogger(__name__)

create_schema = LessonPlanSchema()
update_schema = LessonPlanUpdateSchema()


def _parse_date(value: str | None):
    """Converte string YYYY-MM-DD para date. Retorna None se vazio."""
    if not value:
        return None
    return date.fromisoformat(value)


def list_plans():
    """
    GET /lesson-plans
    Query params:
      page, per_page, search, discipline, tags,
      date_from (YYYY-MM-DD), date_to (YYYY-MM-DD),
      sort_by (title|created_at|planned_date), order (asc|desc)
    """
    try:
        page = max(1, int(request.args.get("page", 1)))
        per_page = min(max(1, int(request.args.get("per_page", 10))), 100)
    except ValueError:
        return jsonify({"error": "Parâmetros de paginação inválidos."}), 400

    try:
        date_from = _parse_date(request.args.get("date_from"))
        date_to = _parse_date(request.args.get("date_to"))
    except ValueError:
        return jsonify({"error": "Datas devem estar no formato YYYY-MM-DD."}), 400

    result = service.list_plans(
        page=page,
        per_page=per_page,
        search=request.args.get("search", "").strip(),
        discipline=request.args.get("discipline", "").strip(),
        tags=request.args.get("tags", "").strip(),
        date_from=date_from,
        date_to=date_to,
        sort_by=request.args.get("sort_by", "created_at"),
        order=request.args.get("order", "desc"),
    )
    return jsonify(result), 200


def get_plan(plan_id):
    plan = service.get_plan(plan_id)
    if plan is None:
        return jsonify({"error": "Plano de aula não encontrado."}), 404
    return jsonify(plan), 200


def create_plan():
    try:
        data = create_schema.load(request.get_json() or {})
    except ValidationError as err:
        return jsonify({"error": "Dados inválidos.", "details": err.messages}), 400

    plan = service.create_plan(data)
    logger.info("Plano criado: id=%s title=%r", plan["id"], plan["title"])
    return jsonify(plan), 201


def update_plan(plan_id):
    try:
        data = update_schema.load(request.get_json() or {})
    except ValidationError as err:
        return jsonify({"error": "Dados inválidos.", "details": err.messages}), 400

    plan = service.update_plan(plan_id, data)
    if plan is None:
        return jsonify({"error": "Plano de aula não encontrado."}), 404
    logger.info("Plano atualizado: id=%s", plan_id)
    return jsonify(plan), 200


def delete_plan(plan_id):
    deleted = service.delete_plan(plan_id)
    if not deleted:
        return jsonify({"error": "Plano de aula não encontrado."}), 404
    logger.info("Plano removido: id=%s", plan_id)
    return jsonify({"message": "Plano de aula removido com sucesso."}), 200
