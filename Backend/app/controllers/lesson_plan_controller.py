from flask import request, jsonify
from marshmallow import ValidationError

from app.schemas.lesson_plan_schema import LessonPlanSchema, LessonPlanUpdateSchema
from app.services import lesson_plan_service as service

create_schema = LessonPlanSchema()
update_schema = LessonPlanUpdateSchema()


def list_plans():
    plans = service.list_plans()
    return jsonify(plans), 200


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
    return jsonify(plan), 201


def update_plan(plan_id):
    try:
        data = update_schema.load(request.get_json() or {})
    except ValidationError as err:
        return jsonify({"error": "Dados inválidos.", "details": err.messages}), 400

    plan = service.update_plan(plan_id, data)
    if plan is None:
        return jsonify({"error": "Plano de aula não encontrado."}), 404
    return jsonify(plan), 200


def delete_plan(plan_id):
    deleted = service.delete_plan(plan_id)
    if not deleted:
        return jsonify({"error": "Plano de aula não encontrado."}), 404
    return jsonify({"message": "Plano de aula removido com sucesso."}), 200
