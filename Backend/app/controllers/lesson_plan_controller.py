import logging

from flask import request, jsonify
from marshmallow import ValidationError

from app.schemas.lesson_plan_schema import (
    LessonPlanSchema,
    LessonPlanUpdateSchema,
    AISuggestionsSchema,
)
from app.services import lesson_plan_service as service
from app.services import ai_service

logger = logging.getLogger(__name__)

create_schema = LessonPlanSchema()
update_schema = LessonPlanUpdateSchema()
ai_schema = AISuggestionsSchema()


def list_plans():
    page = max(1, int(request.args.get("page", 1)))
    limit = min(max(1, int(request.args.get("limit", 10))), 100)
    search = request.args.get("search", "").strip()
    discipline = request.args.get("discipline", "").strip()
    tag = request.args.get("tag", "").strip()
    planned_date = request.args.get("planned_date", "").strip()
    sort = request.args.get("sort", "created_at").strip()

    result = service.list_plans(
        page=page,
        limit=limit,
        search=search,
        discipline=discipline,
        tag=tag,
        planned_date=planned_date,
        sort=sort,
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


def ai_suggestions():
    try:
        data = ai_schema.load(request.get_json() or {})
    except ValidationError as err:
        return jsonify({"error": "Dados inválidos.", "details": err.messages}), 400

    suggestions = ai_service.get_suggestions(
        title=data["title"],
        discipline=data["discipline"],
        summary=data["summary"],
    )
    return jsonify(suggestions), 200
