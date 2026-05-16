from flask import Blueprint
from app.controllers import lesson_plan_controller as controller

lesson_plan_bp = Blueprint("lesson_plans", __name__, url_prefix="/lesson-plans")

lesson_plan_bp.add_url_rule("", view_func=controller.list_plans, methods=["GET"])
lesson_plan_bp.add_url_rule("", view_func=controller.create_plan, methods=["POST"])
lesson_plan_bp.add_url_rule("/<int:plan_id>", view_func=controller.get_plan, methods=["GET"])
lesson_plan_bp.add_url_rule("/<int:plan_id>", view_func=controller.update_plan, methods=["PUT"])
lesson_plan_bp.add_url_rule("/<int:plan_id>", view_func=controller.delete_plan, methods=["DELETE"])
